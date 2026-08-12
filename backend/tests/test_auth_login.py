import json
import os
import socket
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request

from jose import jwt
from uvicorn import Config, Server

from app.main import app
from app.api.v1.auth import reset_rate_limit
from app.core.config import get_settings
from app.core.security import hash_password
from app.db.models import Base, Role, User
from app.db.session import reset_engine, init_engine, SessionLocal


class LiveServer:
    def __init__(self, app):
        self.app = app
        self._port = self._find_free_port()
        self._server = Server(Config(app=self.app, host="127.0.0.1", port=self._port, log_level="critical"))
        self._thread = threading.Thread(target=self._server.run, daemon=True)

    def _find_free_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]

    def start(self):
        self._thread.start()
        url = f"http://127.0.0.1:{self._port}/api/v1/health"
        for _ in range(50):
            try:
                with urllib.request.urlopen(url, timeout=0.5):
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


class AuthLoginTests(unittest.TestCase):
    def setUp(self):
        self.tmp_db = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        self.tmp_db.close()
        db_url = f"sqlite:///{self.tmp_db.name}"
        os.environ["DATABASE_URL"] = db_url
        os.environ["JWT_SECRET_KEY"] = "testsecretkey123"
        os.environ["BOOTSTRAP_ADMIN_PASSWORD"] = "TempP@ss1234"

        reset_engine()
        reset_rate_limit()
        engine = init_engine()
        Base.metadata.create_all(engine)

        with SessionLocal() as session:
            admin_role = Role(role_name="Admin", description="Admin role.")
            session.add(admin_role)
            session.flush()

            admin = User(
                username="admin",
                password_hash=hash_password("TempP@ss1234"),
                full_name="Administrator",
                role=admin_role,
                is_active=True,
            )
            session.add(admin)
            session.commit()

        self.server = LiveServer(app)
        self.server.start()

    def tearDown(self):
        self.server.stop()
        reset_engine()
        os.unlink(self.tmp_db.name)

    def _post_json(self, path, payload):
        url = urllib.parse.urljoin(self.server.base_url, path)
        data = json.dumps(payload).encode("utf-8")
        request_obj = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request_obj, timeout=5) as response:
                body = response.read().decode("utf-8")
                return response.getcode(), json.loads(body)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8")
            return exc.code, json.loads(body)

    def test_successful_login_returns_jwt_and_role(self):
        status, payload = self._post_json(
            "/api/v1/auth/login",
            {"username": "admin", "password": "TempP@ss1234"},
        )

        self.assertEqual(status, 200)
        self.assertEqual(payload["role"], "Admin")
        self.assertIn("access_token", payload)
        self.assertIn("expires_at", payload)

        token = payload["access_token"]
        settings = get_settings()
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

        with SessionLocal() as session:
            admin = session.query(User).filter_by(username="admin").one()

        self.assertEqual(decoded["sub"], str(admin.user_id))
        self.assertEqual(decoded["role"], payload["role"])

    def test_wrong_password_returns_generic_401(self):
        status, payload = self._post_json(
            "/api/v1/auth/login",
            {"username": "admin", "password": "wrongpassword"},
        )
        self.assertEqual(status, 401)
        self.assertEqual(payload, {"detail": "Invalid username or password."})

    def test_nonexistent_user_returns_generic_401(self):
        status, payload = self._post_json(
            "/api/v1/auth/login",
            {"username": "missinguser", "password": "whatever"},
        )
        self.assertEqual(status, 401)
        self.assertEqual(payload, {"detail": "Invalid username or password."})

    def test_missing_username_or_password_returns_400(self):
        status, payload = self._post_json(
            "/api/v1/auth/login",
            {"username": "admin"},
        )
        self.assertEqual(status, 400)

        status, payload = self._post_json(
            "/api/v1/auth/login",
            {"password": "TempP@ss1234"},
        )
        self.assertEqual(status, 400)

    def test_rate_limit_exceeded_after_repeated_failures(self):
        for _ in range(5):
            status, payload = self._post_json(
                "/api/v1/auth/login",
                {"username": "admin", "password": "wrongpassword"},
            )
            self.assertEqual(status, 401)

        status, payload = self._post_json(
            "/api/v1/auth/login",
            {"username": "admin", "password": "wrongpassword"},
        )
        self.assertEqual(status, 429)
        self.assertEqual(payload, {"detail": "Too many login attempts. Please try again later."})
