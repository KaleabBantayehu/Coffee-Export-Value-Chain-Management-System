import json
import os
import socket
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request

from jose import jwt
from uvicorn import Config, Server

from app.api.v1.auth import reset_rate_limit
from app.core.security import create_jwt_token, hash_password
from app.db.models import Base, Role, User
from app.db.session import SessionLocal, init_engine, reset_engine
from app.main import app


class LiveServer:
    def __init__(self, application):
        self._port = self._find_free_port()
        self._server = Server(
            Config(application, host="127.0.0.1", port=self._port, log_level="critical")
        )
        self._thread = threading.Thread(target=self._server.run, daemon=True)

    @staticmethod
    def _find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("127.0.0.1", 0))
            return server_socket.getsockname()[1]

    def start(self):
        self._thread.start()
        health_url = f"http://127.0.0.1:{self._port}/api/v1/health"
        for _ in range(50):
            try:
                with urllib.request.urlopen(health_url, timeout=0.5):
                    return
            except Exception:
                time.sleep(0.1)
        raise RuntimeError("Live server failed to start")

    def stop(self):
        self._server.should_exit = True
        self._thread.join(timeout=5)

    @property
    def base_url(self):
        return f"http://127.0.0.1:{self._port}"


class AuthSessionTests(unittest.TestCase):
    password = "TempP@ss1234"

    def setUp(self):
        self.tmp_db = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        self.tmp_db.close()
        os.environ["DATABASE_URL"] = f"sqlite:///{self.tmp_db.name}"
        os.environ["JWT_SECRET_KEY"] = "testsecretkey123"
        reset_engine()
        reset_rate_limit()
        engine = init_engine()
        Base.metadata.create_all(engine)

        with SessionLocal() as session:
            admin_role = Role(role_name="Admin", description="Admin role.")
            session.add(admin_role)
            session.flush()
            session.add(
                User(
                    username="admin",
                    password_hash=hash_password(self.password),
                    full_name="Administrator",
                    role=admin_role,
                    is_active=True,
                )
            )
            session.commit()

        self.server = LiveServer(app)
        self.server.start()

    def tearDown(self):
        self.server.stop()
        reset_engine()
        os.unlink(self.tmp_db.name)

    def request(self, method, path, token=None):
        request = urllib.request.Request(
            f"{self.server.base_url}{path}",
            headers={"Authorization": f"Bearer {token}"} if token else {},
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read().decode("utf-8"))

    def login(self):
        request = urllib.request.Request(
            f"{self.server.base_url}/api/v1/auth/login",
            data=json.dumps({"username": "admin", "password": self.password}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))["access_token"]

    def test_me_returns_authenticated_profile(self):
        status, payload = self.request("GET", "/api/v1/auth/me", self.login())

        self.assertEqual(status, 200)
        self.assertEqual(
            payload,
            {
                "user_id": 1,
                "username": "admin",
                "full_name": "Administrator",
                "role": "Admin",
            },
        )

    def test_me_rejects_missing_token(self):
        status, payload = self.request("GET", "/api/v1/auth/me")

        self.assertEqual(status, 401)
        self.assertEqual(payload, {"detail": "Invalid authentication token."})

    def test_me_rejects_expired_token(self):
        token, _ = create_jwt_token("1", "Admin", os.environ["JWT_SECRET_KEY"], -1)

        status, payload = self.request("GET", "/api/v1/auth/me", token)

        self.assertEqual(status, 401)
        self.assertEqual(payload, {"detail": "Invalid authentication token."})

    def test_me_rejects_token_signed_with_wrong_secret(self):
        token, _ = create_jwt_token("1", "Admin", "wrong-secret", 30)

        status, payload = self.request("GET", "/api/v1/auth/me", token)

        self.assertEqual(status, 401)
        self.assertEqual(payload, {"detail": "Invalid authentication token."})

    def test_logout_acknowledges_valid_token(self):
        status, payload = self.request("POST", "/api/v1/auth/logout", self.login())

        self.assertEqual(status, 200)
        self.assertEqual(payload, {"detail": "Logout acknowledged."})

    def test_logout_rejects_invalid_token(self):
        status, payload = self.request("POST", "/api/v1/auth/logout", "not-a-jwt")

        self.assertEqual(status, 401)
        self.assertEqual(payload, {"detail": "Invalid authentication token."})


if __name__ == "__main__":
    unittest.main()
