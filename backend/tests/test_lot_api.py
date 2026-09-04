import json
import socket
import threading
import time
import unittest
import urllib.error
import urllib.request
import uuid
from unittest.mock import patch

from geoalchemy2.elements import WKTElement
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from uvicorn import Config, Server

from app.core.config import get_settings
from app.core.identifiers import validate_coffee_lot_gin
from app.core.security import create_jwt_token, hash_password
from app.db.models import CoffeeLot, Farm, Farmer, Role, TraceabilityEvent, User
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


class CoffeeLotApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(get_settings().DATABASE_URL)
        cls.marker = uuid.uuid4().hex[:12]
        cls.created_user_ids: list[int] = []
        cls.created_farmer_ids: list[int] = []
        cls.created_farm_ids: list[int] = []

        with Session(cls.engine) as session:
            cls.roles = {}
            for role_name in ("Admin", "ECTA Officer", "Field/Registry Agent", "Verifier"):
                role = session.query(Role).filter(Role.role_name == role_name).one_or_none()
                if role is None:
                    role = Role(role_name=role_name)
                    session.add(role)
                    session.flush()
                cls.roles[role_name] = role.role_id

            cls.user_ids = {}
            for role_name, role_id in cls.roles.items():
                user = User(
                    username=f"lot-test-{cls.marker}-{role_id}",
                    password_hash=hash_password("TempP@ss1234"),
                    full_name="Coffee Lot API Test",
                    role_id=role_id,
                    is_active=True,
                )
                session.add(user)
                session.flush()
                cls.user_ids[role_name] = user.user_id
                cls.created_user_ids.append(user.user_id)

            farmer = Farmer(
                fin_code=f"LOT-TEST-{cls.marker}",
                full_name="Coffee Lot Test Farmer",
                national_id=f"LOT-NID-{cls.marker}",
            )
            session.add(farmer)
            session.flush()
            cls.created_farmer_ids.append(farmer.farmer_id)
            farm = Farm(
                farmer_id=farmer.farmer_id,
                polygon_geom=WKTElement("POLYGON((38.75 9.00,38.76 9.00,38.77 9.01,38.76 9.02,38.75 9.02,38.74 9.01,38.75 9.00))", srid=4326),
                area_hectares=1.0,
                eudr_risk_flag=False,
            )
            session.add(farm)
            session.flush()
            cls.farm_id = farm.farm_id
            cls.created_farm_ids.append(farm.farm_id)
            session.commit()

        cls.server = LiveServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()
        with cls.engine.begin() as connection:
            connection.execute(TraceabilityEvent.__table__.delete().where(TraceabilityEvent.lot_id.in_(connection.execute(CoffeeLot.__table__.select().with_only_columns(CoffeeLot.lot_id).where(CoffeeLot.farm_id.in_(cls.created_farm_ids))).scalars().all())))
            connection.execute(CoffeeLot.__table__.delete().where(CoffeeLot.farm_id.in_(cls.created_farm_ids)))
            connection.execute(Farm.__table__.delete().where(Farm.farm_id.in_(cls.created_farm_ids)))
            connection.execute(Farmer.__table__.delete().where(Farmer.farmer_id.in_(cls.created_farmer_ids)))
            connection.execute(User.__table__.delete().where(User.user_id.in_(cls.created_user_ids)))
        cls.engine.dispose()

    def token_for(self, role_name: str) -> str:
        return create_jwt_token(str(self.user_ids[role_name]), role_name, get_settings().JWT_SECRET_KEY, 30)[0]

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

    def test_agent_creates_lot_with_gin_and_initial_event(self):
        status, created = self.request("POST", "/api/v1/lots", self.token_for("Field/Registry Agent"), {"farm_id": self.farm_id})

        self.assertEqual(status, 201)
        self.assertTrue(validate_coffee_lot_gin(created["gin_code"]))
        self.assertEqual(created["farm_id"], self.farm_id)
        self.assertEqual(created["created_by"], self.user_ids["Field/Registry Agent"])
        self.assertEqual(created["status"], "created")

        with Session(self.engine) as session:
            events = session.query(TraceabilityEvent).filter(TraceabilityEvent.lot_id == created["lot_id"]).all()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_type, "lot_created")
        self.assertEqual(events[0].recorded_by, self.user_ids["Field/Registry Agent"])

    def test_authorization_and_missing_farm_are_rejected(self):
        status, _ = self.request("POST", "/api/v1/lots", body={"farm_id": self.farm_id})
        self.assertEqual(status, 401)

        status, _ = self.request("POST", "/api/v1/lots", self.token_for("Verifier"), {"farm_id": self.farm_id})
        self.assertEqual(status, 403)

        status, payload = self.request("POST", "/api/v1/lots", self.token_for("Admin"), {"farm_id": 999999999})
        self.assertEqual(status, 404)
        self.assertEqual(payload, {"detail": "Farm 999999999 not found."})

    def test_gin_generation_failure_rolls_back_lot_and_event(self):
        with Session(self.engine) as session:
            before_lots = session.query(CoffeeLot).filter(CoffeeLot.farm_id == self.farm_id).count()
            before_events = session.query(TraceabilityEvent).join(CoffeeLot).filter(CoffeeLot.farm_id == self.farm_id).count()

        with patch("app.services.lot_service.generate_coffee_lot_gin", side_effect=ValueError("GIN retry limit reached")):
            status, payload = self.request("POST", "/api/v1/lots", self.token_for("Admin"), {"farm_id": self.farm_id})

        self.assertEqual(status, 400)
        self.assertEqual(payload, {"detail": "GIN retry limit reached"})
        with Session(self.engine) as session:
            after_lots = session.query(CoffeeLot).filter(CoffeeLot.farm_id == self.farm_id).count()
            after_events = session.query(TraceabilityEvent).join(CoffeeLot).filter(CoffeeLot.farm_id == self.farm_id).count()
        self.assertEqual(after_lots, before_lots)
        self.assertEqual(after_events, before_events)

    def test_any_authenticated_role_can_append_events_in_order(self):
        status, lot = self.request("POST", "/api/v1/lots", self.token_for("Admin"), {"farm_id": self.farm_id})
        self.assertEqual(status, 201)
        for role_name in ("Admin", "ECTA Officer", "Field/Registry Agent", "Verifier"):
            status, event = self.request("POST", f"/api/v1/lots/{lot['lot_id']}/events", self.token_for(role_name), {"event_type": f"{role_name} event", "notes": "Synthetic test event"})
            self.assertEqual(status, 201)
            self.assertEqual(event["recorded_by"], self.user_ids[role_name])
        with Session(self.engine) as session:
            events = session.query(TraceabilityEvent).filter(TraceabilityEvent.lot_id == lot["lot_id"]).order_by(TraceabilityEvent.event_id).all()
        self.assertEqual([event.event_type for event in events][1:], ["Admin event", "ECTA Officer event", "Field/Registry Agent event", "Verifier event"])

    def test_event_auth_validation_and_missing_lot_are_rejected(self):
        status, lot = self.request("POST", "/api/v1/lots", self.token_for("Admin"), {"farm_id": self.farm_id})
        self.assertEqual(status, 201)
        status, _ = self.request("POST", f"/api/v1/lots/{lot['lot_id']}/events", body={"event_type": "Observed"})
        self.assertEqual(status, 401)
        status, _ = self.request("POST", "/api/v1/lots/999999999/events", self.token_for("Verifier"), {"event_type": "Observed"})
        self.assertEqual(status, 404)
        status, _ = self.request("POST", f"/api/v1/lots/{lot['lot_id']}/events", self.token_for("Verifier"), {"event_type": ""})
        self.assertEqual(status, 400)
        status, _ = self.request("POST", f"/api/v1/lots/{lot['lot_id']}/events", self.token_for("Verifier"), {})
        self.assertEqual(status, 400)


if __name__ == "__main__":
    unittest.main()
