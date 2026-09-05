import base64
import hashlib
import json
import os
import socket
import threading
import time
import unittest
import urllib.error
import urllib.request
import uuid

from geoalchemy2.elements import WKTElement
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uvicorn import Config, Server

from app.core.config import get_settings
from app.core.security import create_jwt_token, hash_password
from app.db.models import CoffeeLot, Farm, Farmer, QRRecord, Role, User
from app.main import app
from app.services.qr_service import canonical_payload, sign_payload


class LiveServer:
    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 0))
            self.port = sock.getsockname()[1]
        self.server = Server(Config(app, host="127.0.0.1", port=self.port, log_level="critical"))
        self.thread = threading.Thread(target=self.server.run, daemon=True)

    @property
    def base_url(self): return f"http://127.0.0.1:{self.port}"
    def start(self):
        self.thread.start()
        for _ in range(50):
            try:
                urllib.request.urlopen(f"{self.base_url}/api/v1/health", timeout=.5); return
            except Exception: time.sleep(.1)
        raise RuntimeError("Live server failed to start")
    def stop(self): self.server.should_exit = True; self.thread.join(timeout=5)


class QRGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = {key: os.environ.get(key) for key in ("QR_HMAC_SECRET_KEY", "PUBLIC_QR_BASE_URL")}
        os.environ["QR_HMAC_SECRET_KEY"] = "qr-test-secret"
        os.environ["PUBLIC_QR_BASE_URL"] = "https://demo.example"
        cls.engine = create_engine(get_settings().DATABASE_URL); cls.marker = uuid.uuid4().hex[:10]
        with Session(cls.engine) as s:
            cls.users = {}
            for role_name in ("Admin", "ECTA Officer", "Field/Registry Agent", "Verifier"):
                role = s.query(Role).filter(Role.role_name == role_name).one()
                user = User(username=f"qr-{cls.marker}-{role.role_id}", password_hash=hash_password("TempP@ss1234"), full_name="QR Test", role_id=role.role_id, is_active=True)
                s.add(user); s.flush(); cls.users[role_name] = user.user_id
            farmer = Farmer(fin_code=f"QR-FIN-{cls.marker}", full_name="QR Farmer", national_id=f"QR-NID-{cls.marker}")
            s.add(farmer); s.flush()
            farm = Farm(farmer_id=farmer.farmer_id, polygon_geom=WKTElement("POLYGON((38 9,38.01 9,38.02 9.01,38.01 9.02,38 9.02,37.99 9.01,38 9))", srid=4326), area_hectares=1, eudr_risk_flag=False)
            s.add(farm); s.flush()
            lot = CoffeeLot(gin_code=f"ETH-LOT-2026-{cls.marker[:6]}", farm_id=farm.farm_id, created_by=cls.users["Admin"], status="created")
            s.add(lot); s.commit(); cls.lot_id = lot.lot_id; cls.farm_id = farm.farm_id; cls.farmer_id = farmer.farmer_id
        cls.server = LiveServer(); cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()
        with cls.engine.begin() as c:
            c.execute(QRRecord.__table__.delete().where(QRRecord.lot_id == cls.lot_id)); c.execute(CoffeeLot.__table__.delete().where(CoffeeLot.lot_id == cls.lot_id)); c.execute(Farm.__table__.delete().where(Farm.farm_id == cls.farm_id)); c.execute(Farmer.__table__.delete().where(Farmer.farmer_id == cls.farmer_id)); c.execute(User.__table__.delete().where(User.user_id.in_(cls.users.values())))
        cls.engine.dispose()
        for key, value in cls.env.items():
            if value is None: os.environ.pop(key, None)
            else: os.environ[key] = value

    def token(self, role): return create_jwt_token(str(self.users[role]), role, get_settings().JWT_SECRET_KEY, 30)[0]
    def request(self, method, path, token=None, body=None):
        data = json.dumps(body).encode() if body is not None else None; headers = {"Content-Type": "application/json"} if data else {}
        if token: headers["Authorization"] = f"Bearer {token}"
        try:
            with urllib.request.urlopen(urllib.request.Request(f"{self.server.base_url}{path}", data=data, headers=headers, method=method), timeout=10) as response: return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error: return error.code, json.loads(error.read())

    def test_canonical_payload_and_hmac(self):
        payload = canonical_payload(123, "ETH-LOT-2026-000001", __import__("datetime").datetime(2026, 9, 5, 10))
        self.assertEqual(payload, b'{"v":1,"qrId":123,"gin":"ETH-LOT-2026-000001","issuedAt":"2026-09-05T10:00:00Z"}')
        signature = sign_payload(payload, "fixed-key")
        self.assertEqual(signature, sign_payload(payload, "fixed-key")); self.assertNotEqual(signature, sign_payload(payload + b"x", "fixed-key")); self.assertNotIn("=", signature)
        self.assertEqual(hashlib.sha256(payload).hexdigest(), hashlib.sha256(payload).hexdigest())

    def test_generation_rbac_lifecycle_and_images(self):
        for role in ("ECTA Officer", "Verifier"):
            self.assertEqual(self.request("POST", f"/api/v1/lots/{self.lot_id}/qr", self.token(role), {})[0], 403)
        self.assertEqual(self.request("POST", f"/api/v1/lots/{self.lot_id}/qr", body={})[0], 401)
        status, first = self.request("POST", f"/api/v1/lots/{self.lot_id}/qr", self.token("Admin"), {})
        self.assertEqual(status, 201); self.assertTrue(first["image_svg"].startswith("data:image/svg+xml;base64,")); self.assertTrue(first["image_png_data_url"].startswith("data:image/png;base64,")); self.assertIn(b"<svg", base64.b64decode(first["image_svg"].split(",", 1)[1])); self.assertEqual(base64.b64decode(first["image_png_data_url"].split(",", 1)[1])[:8], b"\x89PNG\r\n\x1a\n"); self.assertNotIn("payload_hash", first); self.assertNotIn("hmac_signature", first)
        status, same = self.request("POST", f"/api/v1/lots/{self.lot_id}/qr", self.token("Field/Registry Agent"), {})
        self.assertEqual(status, 200); self.assertEqual(same["qr_id"], first["qr_id"])
        status, next_record = self.request("POST", f"/api/v1/lots/{self.lot_id}/qr", self.token("Admin"), {"regenerate": True})
        self.assertEqual(status, 201); self.assertNotEqual(next_record["qr_id"], first["qr_id"])
        with Session(self.engine) as s:
            records = s.query(QRRecord).filter(QRRecord.lot_id == self.lot_id).all()
            self.assertEqual(len([record for record in records if record.is_active]), 1); self.assertFalse(next(record for record in records if record.qr_id == first["qr_id"]).is_active)
            active = next(record for record in records if record.is_active)
            expected = canonical_payload(active.qr_id, f"ETH-LOT-2026-{self.marker[:6]}", active.generated_at)
            self.assertEqual(active.payload_hash, hashlib.sha256(expected).hexdigest())
            with self.assertRaises(IntegrityError), s.begin_nested():
                s.add(QRRecord(lot_id=self.lot_id, payload_hash="x", hmac_signature="x", verification_url="https://invalid", is_active=True))
                s.flush()

    def test_missing_lot_and_malformed_body(self):
        self.assertEqual(self.request("POST", "/api/v1/lots/999999999/qr", self.token("Admin"), {})[0], 404)
        self.assertEqual(self.request("POST", f"/api/v1/lots/{self.lot_id}/qr", self.token("Admin"), {"regenerate": "bad"})[0], 400)
