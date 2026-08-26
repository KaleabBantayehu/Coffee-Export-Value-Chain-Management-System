import json
import os
import socket
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request

from uvicorn import Config, Server

from app.api.v1.auth import reset_rate_limit
from app.core.security import create_jwt_token, hash_password
from app.db.models import Base, Permission, Role, User
from app.db.session import SessionLocal, init_engine, reset_engine
from app.main import app

AUTH_TABLES = [Base.metadata.tables[name] for name in ("roles", "permissions", "role_permission", "users")]


class LiveServer:
    def __init__(self, application):
        self._port = self._find_free_port()
        self._server = Server(Config(application, host="127.0.0.1", port=self._port, log_level="critical"))
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


class RbacTests(unittest.TestCase):
    def setUp(self):
        self.env_backup = dict(os.environ)
        self.tmp_db = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        self.tmp_db.close()
        os.environ["DATABASE_URL"] = f"sqlite:///{self.tmp_db.name}"
        os.environ["JWT_SECRET_KEY"] = "testsecretkey123"
        reset_engine()
        reset_rate_limit()
        Base.metadata.create_all(init_engine(), tables=AUTH_TABLES)

        with SessionLocal() as session:
            admin_role = Role(role_name="Admin")
            agent_role = Role(role_name="Field/Registry Agent")
            manage_users = Permission(permission_code="users:manage")
            admin_role.permissions.append(manage_users)
            session.add_all([admin_role, agent_role])
            session.flush()
            session.add_all([
                User(username="admin", password_hash=hash_password("TempP@ss1234"), full_name="Administrator", role=admin_role),
                User(username="agent", password_hash=hash_password("TempP@ss1234"), full_name="Field Agent", role=agent_role),
            ])
            session.commit()

        self.server = LiveServer(app)
        self.server.start()

    def tearDown(self):
        self.server.stop()
        reset_engine()
        os.unlink(self.tmp_db.name)
        os.environ.clear()
        os.environ.update(self.env_backup)

    def request(self, token=None):
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        request = urllib.request.Request(f"{self.server.base_url}/api/v1/users", headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read().decode("utf-8"))

    def token_for_user(self, user_id, claimed_role):
        return create_jwt_token(str(user_id), claimed_role, os.environ["JWT_SECRET_KEY"], 30)[0]

    def test_admin_with_seeded_permission_can_list_users(self):
        status, payload = self.request(self.token_for_user(1, "Admin"))

        self.assertEqual(status, 200)
        self.assertEqual([user["username"] for user in payload], ["admin", "agent"])

    def test_authenticated_user_without_seeded_permission_is_forbidden(self):
        status, payload = self.request(self.token_for_user(2, "Field/Registry Agent"))

        self.assertEqual(status, 403)
        self.assertEqual(payload, {"detail": "Not authorized."})

    def test_unauthenticated_request_is_rejected_before_authorization(self):
        status, payload = self.request()

        self.assertEqual(status, 401)
        self.assertEqual(payload, {"detail": "Invalid authentication token."})

    def test_database_permissions_are_used_instead_of_the_jwt_role_claim(self):
        status, payload = self.request(self.token_for_user(2, "Admin"))

        self.assertEqual(status, 403)
        self.assertEqual(payload, {"detail": "Not authorized."})


if __name__ == "__main__":
    unittest.main()
