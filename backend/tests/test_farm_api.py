import json
import socket
import threading
import time
import unittest
import urllib.error
import urllib.request
import uuid

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from uvicorn import Config, Server

from app.core.config import get_settings
from app.core.security import create_jwt_token, hash_password
from app.db.models import Farmer, Role, User
from app.main import app


class LiveServer:
    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("127.0.0.1", 0))
            self._port = server_socket.getsockname()[1]
        self._server = Server(Config(app, host="127.0.0.1", port=self._port, log_level="critical"))
        self._thread = threading.Thread(target=self._server.run, daemon=True)

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self._port}"

    def start(self) -> None:
        self._thread.start()
        for _ in range(50):
            try:
                with urllib.request.urlopen(f"{self.base_url}/api/v1/health", timeout=0.5):
                    return
            except Exception:
                time.sleep(0.1)
        raise RuntimeError("Live server failed to start")

    def stop(self) -> None:
        self._server.should_exit = True
        self._thread.join(timeout=5)


class FarmApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(get_settings().DATABASE_URL)
        cls.marker = uuid.uuid4().hex[:12]
        cls.farmer_ids: list[int] = []
        cls.user_ids: list[int] = []

        with Session(cls.engine) as session:
            roles = {}
            for role_name in ("Admin", "Field/Registry Agent", "Verifier"):
                role = session.query(Role).filter_by(role_name=role_name).one_or_none()
                if role is None:
                    role = Role(role_name=role_name)
                    session.add(role)
                    session.flush()
                roles[role_name] = role

            cls.users = {}
            for role_name, role in roles.items():
                user = User(
                    username=f"farm-test-{cls.marker}-{role.role_id}",
                    password_hash=hash_password("TempP@ss1234"),
                    full_name="Farm API Test",
                    role_id=role.role_id,
                    is_active=True,
                )
                session.add(user)
                session.flush()
                cls.users[role_name] = user.user_id
                cls.user_ids.append(user.user_id)
            session.commit()

        cls.server = LiveServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()
        with cls.engine.begin() as connection:
            if cls.farmer_ids:
                connection.execute(text("DELETE FROM farms WHERE farmer_id = ANY(:farmer_ids)"), {"farmer_ids": cls.farmer_ids})
                connection.execute(text("DELETE FROM farmers WHERE farmer_id = ANY(:farmer_ids)"), {"farmer_ids": cls.farmer_ids})
            if cls.user_ids:
                connection.execute(text("DELETE FROM users WHERE user_id = ANY(:user_ids)"), {"user_ids": cls.user_ids})
        cls.engine.dispose()

    def token_for(self, role_name: str) -> str:
        return create_jwt_token(str(self.users[role_name]), role_name, get_settings().JWT_SECRET_KEY, 30)[0]

    def request(self, method: str, path: str, token: str | None = None, body: dict | None = None):
        data = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {"Content-Type": "application/json"} if data is not None else {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(f"{self.server.base_url}{path}", data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read().decode("utf-8"))

    def new_farmer(self) -> int:
        with Session(self.engine) as session:
            farmer = Farmer(
                fin_code=f"FARM-TEST-{uuid.uuid4().hex}",
                full_name="Farm Test Farmer",
                national_id=f"NID-{uuid.uuid4().hex}",
            )
            session.add(farmer)
            session.commit()
            self.farmer_ids.append(farmer.farmer_id)
            return farmer.farmer_id

    @staticmethod
    def polygon() -> dict:
        return {
            "type": "Polygon",
            "coordinates": [[[38.75, 9.00], [38.76, 9.00], [38.77, 9.01], [38.76, 9.02], [38.75, 9.02], [38.74, 9.01], [38.75, 9.00]]],
        }

    def test_agent_creates_polygon_and_geojson_round_trips_as_postgis(self):
        farmer_id = self.new_farmer()
        status, created = self.request(
            "POST", "/api/v1/farms", self.token_for("Field/Registry Agent"), {"farmer_id": farmer_id, "geometry": self.polygon()}
        )
        self.assertEqual(status, 201)
        self.assertEqual(created["geometry"], self.polygon())
        self.assertIsNone(created["area_hectares"])
        self.assertIsNone(created["eudr_risk_flag"])

        status, retrieved = self.request("GET", f"/api/v1/farms/{created['farm_id']}", self.token_for("Verifier"))
        self.assertEqual(status, 200)
        self.assertEqual(retrieved["geometry"], self.polygon())

        with self.engine.connect() as connection:
            geometry_type, srid, area_is_null, risk_is_null = connection.execute(
                text("SELECT GeometryType(polygon_geom), ST_SRID(polygon_geom), area_hectares IS NULL, eudr_risk_flag IS NULL FROM farms WHERE farm_id = :farm_id"),
                {"farm_id": created["farm_id"]},
            ).one()
        self.assertEqual(geometry_type, "POLYGON")
        self.assertEqual(srid, 4326)
        self.assertTrue(area_is_null)
        self.assertTrue(risk_is_null)

    def test_agent_creates_point_plus_radius_farm(self):
        status, created = self.request(
            "POST",
            "/api/v1/farms",
            self.token_for("Field/Registry Agent"),
            {"farmer_id": self.new_farmer(), "geometry": {"type": "Point", "coordinates": [38.75, 9.00]}, "radius_meters": 25},
        )
        self.assertEqual(status, 201)
        self.assertEqual(created["geometry"]["type"], "Polygon")
        self.assertIsNone(created["area_hectares"])
        self.assertIsNone(created["eudr_risk_flag"])

    def test_invalid_geometry_missing_farmer_and_authorization_are_rejected(self):
        farmer_id = self.new_farmer()
        short_polygon = {"type": "Polygon", "coordinates": [[[38.75, 9.00], [38.76, 9.00], [38.76, 9.01], [38.75, 9.00]]]}
        status, payload = self.request("POST", "/api/v1/farms", self.token_for("Field/Registry Agent"), {"farmer_id": farmer_id, "geometry": short_polygon})
        self.assertEqual(status, 400)
        self.assertIn("six vertices", payload["detail"])

        status, _ = self.request("POST", "/api/v1/farms", self.token_for("Field/Registry Agent"), {"farmer_id": 999999999, "geometry": self.polygon()})
        self.assertEqual(status, 404)

        status, _ = self.request(
            "POST",
            "/api/v1/farms",
            self.token_for("Field/Registry Agent"),
            {"farmer_id": farmer_id, "geometry": {"type": "Point", "coordinates": [38.75, 9.00]}},
        )
        self.assertEqual(status, 400)

        status, _ = self.request("POST", "/api/v1/farms", self.token_for("Verifier"), {"farmer_id": farmer_id, "geometry": self.polygon()})
        self.assertEqual(status, 403)
        status, _ = self.request("POST", "/api/v1/farms", body={"farmer_id": farmer_id, "geometry": self.polygon()})
        self.assertEqual(status, 401)
        status, _ = self.request("GET", "/api/v1/farms/999999999", self.token_for("Admin"))
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
