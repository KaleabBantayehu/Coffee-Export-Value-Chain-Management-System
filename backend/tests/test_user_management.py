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
from app.core.security import create_jwt_token, hash_password, verify_password
from app.db.models import AuditLog, Base, Permission, Role, User
from app.db.session import SessionLocal, init_engine, reset_engine
from app.main import app
from app.services.user_service import ROLE_CHANGE_ACTION

# audit_logs is required in addition to the auth tables for the role-change test.
MANAGEMENT_TABLES = [
    Base.metadata.tables[name]
    for name in ("roles", "permissions", "role_permission", "users", "audit_logs")
]

ADMIN_USER_ID = 1
AGENT_USER_ID = 2


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


class UserManagementTests(unittest.TestCase):
    password = "TempP@ss1234"

    def setUp(self):
        self.env_backup = dict(os.environ)
        self.tmp_db = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        self.tmp_db.close()
        os.environ["DATABASE_URL"] = f"sqlite:///{self.tmp_db.name}"
        os.environ["JWT_SECRET_KEY"] = "testsecretkey123"
        reset_engine()
        reset_rate_limit()
        Base.metadata.create_all(init_engine(), tables=MANAGEMENT_TABLES)

        with SessionLocal() as session:
            manage_users = Permission(permission_code="users:manage")
            admin_role = Role(role_name="Admin")
            admin_role.permissions.append(manage_users)
            officer_role = Role(role_name="ECTA Officer")
            agent_role = Role(role_name="Field/Registry Agent")
            verifier_role = Role(role_name="Verifier")
            session.add_all([admin_role, officer_role, agent_role, verifier_role])
            session.flush()
            # Seeded so user ids are deterministic: admin=1, agent=2.
            session.add_all(
                [
                    User(username="admin", password_hash=hash_password(self.password), full_name="Administrator", role=admin_role),
                    User(username="agent", password_hash=hash_password(self.password), full_name="Field Agent", role=agent_role),
                ]
            )
            session.commit()

        self.server = LiveServer(app)
        self.server.start()

    def tearDown(self):
        self.server.stop()
        reset_engine()
        os.unlink(self.tmp_db.name)
        os.environ.clear()
        os.environ.update(self.env_backup)

    def token_for(self, user_id, role="Admin"):
        # The role claim is irrelevant to authorization (RBAC reads DB
        # permissions by user id); user_id selects the acting account.
        return create_jwt_token(str(user_id), role, os.environ["JWT_SECRET_KEY"], 30)[0]

    def request(self, method, path, token=None, body=None):
        data = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if data is not None:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(f"{self.server.base_url}{path}", data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read().decode("utf-8"))

    # --- GET /users ---------------------------------------------------------

    def test_admin_can_list_users_paginated(self):
        status, payload = self.request("GET", "/api/v1/users", self.token_for(ADMIN_USER_ID))

        self.assertEqual(status, 200)
        self.assertEqual([user["username"] for user in payload["items"]], ["admin", "agent"])
        self.assertEqual(payload["total"], 2)
        self.assertEqual(payload["page"], 1)
        self.assertEqual(payload["page_size"], 20)
        # No password material is exposed in the list.
        for user in payload["items"]:
            self.assertNotIn("password", user)
            self.assertNotIn("password_hash", user)

    def test_list_users_respects_page_and_page_size(self):
        with SessionLocal() as session:
            agent_role = session.query(Role).filter_by(role_name="Field/Registry Agent").one()
            session.add_all(
                [
                    User(username=f"extra{i}", password_hash=hash_password(self.password), full_name=f"Extra {i}", role=agent_role)
                    for i in range(3)
                ]
            )
            session.commit()  # total users now 5

        token = self.token_for(ADMIN_USER_ID)
        status, first = self.request("GET", "/api/v1/users?page=1&page_size=2", token)
        self.assertEqual(status, 200)
        self.assertEqual([u["username"] for u in first["items"]], ["admin", "agent"])
        self.assertEqual(first["total"], 5)

        status, third = self.request("GET", "/api/v1/users?page=3&page_size=2", token)
        self.assertEqual(status, 200)
        self.assertEqual(len(third["items"]), 1)
        self.assertEqual(third["total"], 5)
        self.assertEqual(third["page"], 3)

    def test_non_admin_cannot_list_users(self):
        status, payload = self.request("GET", "/api/v1/users", self.token_for(AGENT_USER_ID))

        self.assertEqual(status, 403)
        self.assertEqual(payload, {"detail": "Not authorized."})

    def test_unauthenticated_cannot_list_users(self):
        status, payload = self.request("GET", "/api/v1/users")

        self.assertEqual(status, 401)
        self.assertEqual(payload, {"detail": "Invalid authentication token."})

    # --- POST /users --------------------------------------------------------

    def test_admin_can_create_user_and_password_is_hashed(self):
        new_password = "N3wUserP@ss!"
        status, payload = self.request(
            "POST",
            "/api/v1/users",
            self.token_for(ADMIN_USER_ID),
            {"username": "newagent", "password": new_password, "full_name": "New Agent", "role": "Field/Registry Agent"},
        )

        self.assertEqual(status, 201)
        self.assertEqual(payload["username"], "newagent")
        self.assertEqual(payload["role"], "Field/Registry Agent")
        # Response never carries password material.
        self.assertNotIn("password", payload)
        self.assertNotIn("password_hash", payload)

        with SessionLocal() as session:
            created = session.query(User).filter_by(username="newagent").one()
            self.assertNotEqual(created.password_hash, new_password)
            self.assertTrue(created.password_hash.startswith("$2"))
            self.assertTrue(verify_password(new_password, created.password_hash))

    def test_create_user_with_duplicate_username_is_rejected_structured(self):
        status, payload = self.request(
            "POST",
            "/api/v1/users",
            self.token_for(ADMIN_USER_ID),
            {"username": "admin", "password": "whatever123", "full_name": "Clashing", "role": "Admin"},
        )

        self.assertEqual(status, 409)
        self.assertEqual(payload, {"detail": "Username already exists."})

    def test_create_user_with_invalid_role_is_rejected(self):
        status, payload = self.request(
            "POST",
            "/api/v1/users",
            self.token_for(ADMIN_USER_ID),
            {"username": "someone", "password": "whatever123", "full_name": "Someone", "role": "Overlord"},
        )

        self.assertEqual(status, 400)
        self.assertEqual(payload, {"detail": "Invalid role."})

    def test_create_user_missing_field_returns_400(self):
        status, _ = self.request(
            "POST",
            "/api/v1/users",
            self.token_for(ADMIN_USER_ID),
            {"username": "nopass", "full_name": "No Password", "role": "Admin"},
        )

        self.assertEqual(status, 400)

    def test_non_admin_cannot_create_user(self):
        status, payload = self.request(
            "POST",
            "/api/v1/users",
            self.token_for(AGENT_USER_ID),
            {"username": "sneaky", "password": "whatever123", "full_name": "Sneaky", "role": "Admin"},
        )

        self.assertEqual(status, 403)
        self.assertEqual(payload, {"detail": "Not authorized."})

    def test_unauthenticated_cannot_create_user(self):
        status, _ = self.request(
            "POST",
            "/api/v1/users",
            None,
            {"username": "sneaky", "password": "whatever123", "full_name": "Sneaky", "role": "Admin"},
        )

        self.assertEqual(status, 401)

    # --- PATCH /users/{id}/role --------------------------------------------

    def test_admin_can_change_role_and_audit_log_is_written(self):
        status, payload = self.request(
            "PATCH",
            f"/api/v1/users/{AGENT_USER_ID}/role",
            self.token_for(ADMIN_USER_ID),
            {"role": "ECTA Officer"},
        )

        self.assertEqual(status, 200)
        self.assertEqual(payload["user_id"], AGENT_USER_ID)
        self.assertEqual(payload["role"], "ECTA Officer")

        with SessionLocal() as session:
            entries = session.query(AuditLog).all()
            self.assertEqual(len(entries), 1)
            entry = entries[0]
            self.assertEqual(entry.user_id, ADMIN_USER_ID)  # acting admin
            self.assertEqual(entry.action, ROLE_CHANGE_ACTION)
            self.assertEqual(entry.entity_type, "User")
            self.assertEqual(entry.entity_id, AGENT_USER_ID)
            self.assertEqual(entry.old_value, "Field/Registry Agent")
            self.assertEqual(entry.new_value, "ECTA Officer")
            self.assertIsNotNone(entry.timestamp)
            # The role change itself persisted.
            self.assertEqual(session.get(User, AGENT_USER_ID).role.role_name, "ECTA Officer")

    def test_change_role_to_invalid_role_is_rejected_and_writes_no_audit(self):
        status, payload = self.request(
            "PATCH",
            f"/api/v1/users/{AGENT_USER_ID}/role",
            self.token_for(ADMIN_USER_ID),
            {"role": "Overlord"},
        )

        self.assertEqual(status, 400)
        self.assertEqual(payload, {"detail": "Invalid role."})
        with SessionLocal() as session:
            self.assertEqual(session.query(AuditLog).count(), 0)
            # Original role untouched.
            self.assertEqual(session.get(User, AGENT_USER_ID).role.role_name, "Field/Registry Agent")

    def test_change_role_for_nonexistent_user_returns_404(self):
        status, payload = self.request(
            "PATCH",
            "/api/v1/users/9999/role",
            self.token_for(ADMIN_USER_ID),
            {"role": "Admin"},
        )

        self.assertEqual(status, 404)
        self.assertEqual(payload, {"detail": "User not found."})

    def test_non_admin_cannot_change_role(self):
        status, payload = self.request(
            "PATCH",
            f"/api/v1/users/{ADMIN_USER_ID}/role",
            self.token_for(AGENT_USER_ID),
            {"role": "Verifier"},
        )

        self.assertEqual(status, 403)
        self.assertEqual(payload, {"detail": "Not authorized."})
        with SessionLocal() as session:
            self.assertEqual(session.query(AuditLog).count(), 0)

    def test_unauthenticated_cannot_change_role(self):
        status, _ = self.request(
            "PATCH",
            f"/api/v1/users/{AGENT_USER_ID}/role",
            None,
            {"role": "Verifier"},
        )

        self.assertEqual(status, 401)


if __name__ == "__main__":
    unittest.main()
