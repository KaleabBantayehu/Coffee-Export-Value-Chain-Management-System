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
from app.core.identifiers import validate_farmer_fin
from app.core.security import create_jwt_token, hash_password
from app.db.models import AuditLog, Base, Cooperative, Farmer, Role, User
from app.db.session import SessionLocal, init_engine, reset_engine
from app.main import app

FARMER_TABLES = [
    Base.metadata.tables[name]
    for name in ("roles", "permissions", "role_permission", "users", "cooperatives", "farmers", "audit_logs")
]


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


class FarmerApiTests(unittest.TestCase):
    def setUp(self):
        self.env_backup = dict(os.environ)
        self.tmp_db = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        self.tmp_db.close()
        os.environ["DATABASE_URL"] = f"sqlite:///{self.tmp_db.name}"
        os.environ["JWT_SECRET_KEY"] = "testsecretkey123"
        reset_engine()
        reset_rate_limit()
        Base.metadata.create_all(init_engine(), tables=FARMER_TABLES)

        with SessionLocal() as session:
            admin_role = Role(role_name="Admin")
            agent_role = Role(role_name="Field/Registry Agent")
            verifier_role = Role(role_name="Verifier")
            cooperative = Cooperative(name="Addis Cooperative", region="Addis Ababa")
            session.add_all([admin_role, agent_role, verifier_role, cooperative])
            session.flush()
            session.add_all(
                [
                    User(username="admin", password_hash=hash_password("TempP@ss1234"), full_name="Administrator", role=admin_role),
                    User(username="agent", password_hash=hash_password("TempP@ss1234"), full_name="Field Agent", role=agent_role),
                    User(username="verifier", password_hash=hash_password("TempP@ss1234"), full_name="Verifier", role=verifier_role),
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

    def token_for(self, user_id, role):
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
                payload = response.read().decode("utf-8")
                return response.status, json.loads(payload) if payload else None
        except urllib.error.HTTPError as error:
            payload = error.read().decode("utf-8")
            return error.code, json.loads(payload) if payload else None

    def test_agent_can_register_farmer_and_receives_generated_fin(self):
        status, payload = self.request(
            "POST",
            "/api/v1/farmers",
            token=self.token_for(2, "Field/Registry Agent"),
            body={
                "full_name": "Bekele Tadesse",
                "national_id": "NAT-1001",
                "gender": "Male",
                "phone_number": "+251911000111",
                "cooperative_id": 1,
            },
        )

        self.assertEqual(status, 201)
        self.assertTrue(validate_farmer_fin(payload["fin_code"]))
        self.assertEqual(payload["full_name"], "Bekele Tadesse")
        self.assertEqual(payload["national_id"], "NAT-1001")

    def test_non_field_agent_or_admin_cannot_register_farmer(self):
        status, payload = self.request(
            "POST",
            "/api/v1/farmers",
            token=self.token_for(3, "Verifier"),
            body={
                "full_name": "Verifier User",
                "national_id": "NAT-2001",
                "gender": "Female",
                "phone_number": "+251922000222",
            },
        )

        self.assertEqual(status, 403)
        self.assertEqual(payload, {"detail": "Not authorized."})

    def test_unauthenticated_request_rejected(self):
        status, payload = self.request(
            "POST",
            "/api/v1/farmers",
            body={
                "full_name": "Anon User",
                "national_id": "NAT-3001",
                "gender": "Female",
                "phone_number": "+251933000333",
            },
        )

        self.assertEqual(status, 401)
        self.assertEqual(payload, {"detail": "Invalid authentication token."})

    def test_duplicate_national_id_is_rejected_structured(self):
        self.request(
            "POST",
            "/api/v1/farmers",
            token=self.token_for(2, "Field/Registry Agent"),
            body={
                "full_name": "First Farmer",
                "national_id": "NAT-DUP-1",
                "gender": "Male",
                "phone_number": "+251944000444",
            },
        )

        status, payload = self.request(
            "POST",
            "/api/v1/farmers",
            token=self.token_for(2, "Field/Registry Agent"),
            body={
                "full_name": "Second Farmer",
                "national_id": "NAT-DUP-1",
                "gender": "Female",
                "phone_number": "+251955000555",
            },
        )

        self.assertEqual(status, 409)
        self.assertIn("National ID already exists.", payload["detail"])

    def test_missing_required_field_is_rejected(self):
        status, payload = self.request(
            "POST",
            "/api/v1/farmers",
            token=self.token_for(2, "Field/Registry Agent"),
            body={
                "full_name": "Missing Phone",
                "national_id": "NAT-4001",
                "gender": "Male",
            },
        )

        self.assertEqual(status, 400)

    def test_get_farmer_by_id_succeeds_and_missing_returns_404(self):
        status, payload = self.request(
            "POST",
            "/api/v1/farmers",
            token=self.token_for(2, "Field/Registry Agent"),
            body={
                "full_name": "Abebe Bekele",
                "national_id": "NAT-5001",
                "gender": "Male",
                "phone_number": "+251966000666",
            },
        )
        farmer_id = payload["farmer_id"]

        status, detail = self.request("GET", f"/api/v1/farmers/{farmer_id}", token=self.token_for(1, "Admin"))
        self.assertEqual(status, 200)
        self.assertEqual(detail["farmer_id"], farmer_id)
        self.assertEqual(detail["linked_farms"], [])
        self.assertEqual(detail["farms"], [])

        status, payload = self.request("GET", "/api/v1/farmers/999999", token=self.token_for(1, "Admin"))
        self.assertEqual(status, 404)
        self.assertEqual(payload, {"detail": "Farmer not found."})

    def test_update_farmer_requires_authorized_role_and_writes_audit_log(self):
        status, payload = self.request(
            "POST",
            "/api/v1/farmers",
            token=self.token_for(2, "Field/Registry Agent"),
            body={
                "full_name": "Old Name",
                "national_id": "NAT-6001",
                "gender": "Male",
                "phone_number": "+251977000777",
            },
        )
        farmer_id = payload["farmer_id"]

        status, payload = self.request(
            "PUT",
            f"/api/v1/farmers/{farmer_id}",
            token=self.token_for(2, "Field/Registry Agent"),
            body={
                "full_name": "Updated Name",
                "national_id": "NAT-6001",
                "gender": "Female",
                "phone_number": "+251988000888",
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["full_name"], "Updated Name")

        status, payload = self.request(
            "PUT",
            f"/api/v1/farmers/{farmer_id}",
            token=self.token_for(3, "Verifier"),
            body={
                "full_name": "Blocked Update",
                "national_id": "NAT-6002",
                "gender": "Male",
                "phone_number": "+251999000999",
            },
        )
        self.assertEqual(status, 403)

        with SessionLocal() as session:
            audit_log = session.query(AuditLog).filter_by(entity_type="Farmer", entity_id=farmer_id).one()
            self.assertEqual(audit_log.action, "update_farmer")
            self.assertIn("Old Name", audit_log.old_value)
            self.assertIn("Updated Name", audit_log.new_value)

    def test_search_by_fin_name_and_cooperative(self):
        self.request(
            "POST",
            "/api/v1/farmers",
            token=self.token_for(2, "Field/Registry Agent"),
            body={
                "full_name": "Aster Ababa",
                "national_id": "NAT-7001",
                "gender": "Female",
                "phone_number": "+251901000111",
                "cooperative_id": 1,
            },
        )

        self.request(
            "POST",
            "/api/v1/farmers",
            token=self.token_for(2, "Field/Registry Agent"),
            body={
                "full_name": "Bonsa Bekele",
                "national_id": "NAT-7002",
                "gender": "Male",
                "phone_number": "+251902000222",
            },
        )

        token = self.token_for(1, "Admin")
        status, payload = self.request("GET", "/api/v1/farmers?search=Aster", token=token)
        self.assertEqual(status, 200)
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["full_name"], "Aster Ababa")

        status, payload = self.request("GET", "/api/v1/farmers?search=Addis", token=token)
        self.assertEqual(status, 200)
        self.assertTrue(any(item["cooperative_id"] == 1 for item in payload))

        status, payload = self.request("GET", "/api/v1/farmers?search=ETH-FAR", token=token)
        self.assertEqual(status, 200)
        self.assertGreaterEqual(len(payload), 2)


if __name__ == "__main__":
    unittest.main()
