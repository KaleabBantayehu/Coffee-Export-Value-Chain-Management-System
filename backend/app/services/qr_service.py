import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone
from io import BytesIO

import segno
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import CoffeeLot, QRRecord


class QRServiceError(Exception): pass
class QRLotNotFoundError(QRServiceError): pass
class QRConfigurationError(QRServiceError): pass


def canonical_payload(qr_id: int, gin: str, issued_at: datetime) -> bytes:
    timestamp = issued_at.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return json.dumps({"v": 1, "qrId": qr_id, "gin": gin, "issuedAt": timestamp}, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def sign_payload(payload: bytes, secret: str) -> str:
    return base64.urlsafe_b64encode(hmac.new(secret.encode(), payload, hashlib.sha256).digest()).rstrip(b"=").decode()


def _images(url: str) -> tuple[str, str]:
    code = segno.make(url)
    svg, png = BytesIO(), BytesIO()
    code.save(svg, kind="svg", scale=5)
    code.save(png, kind="png", scale=5)
    return ("data:image/svg+xml;base64," + base64.b64encode(svg.getvalue()).decode(), "data:image/png;base64," + base64.b64encode(png.getvalue()).decode())


def _response(record: QRRecord) -> dict:
    svg, png = _images(record.verification_url)
    return {"qr_id": record.qr_id, "verification_url": record.verification_url, "image_svg": svg, "image_png_data_url": png}


def generate_qr(session: Session, *, lot_id: int, regenerate: bool) -> tuple[dict, bool]:
    settings = get_settings()
    if not settings.QR_HMAC_SECRET_KEY or not settings.PUBLIC_QR_BASE_URL:
        raise QRConfigurationError("QR generation is unavailable.")
    lot = session.query(CoffeeLot).filter(CoffeeLot.lot_id == lot_id).one_or_none()
    if lot is None: raise QRLotNotFoundError(f"Coffee Lot {lot_id} not found.")
    active = session.query(QRRecord).filter(QRRecord.lot_id == lot_id, QRRecord.is_active.is_(True)).one_or_none()
    if active and not regenerate:
        return _response(active), False
    try:
        if active: active.is_active = False
        generated_at = datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)
        record = QRRecord(lot_id=lot_id, payload_hash="", hmac_signature="", verification_url="", generated_at=generated_at, is_active=True)
        session.add(record); session.flush()
        payload = canonical_payload(record.qr_id, lot.gin_code, generated_at)
        signature = sign_payload(payload, settings.QR_HMAC_SECRET_KEY)
        record.payload_hash = hashlib.sha256(payload).hexdigest()
        record.hmac_signature = signature
        record.verification_url = f"{settings.PUBLIC_QR_BASE_URL.rstrip('/')}/verify/{record.qr_id}?sig={signature}"
        result = _response(record)
        session.commit(); session.refresh(record)
        return result, True
    except Exception:
        session.rollback(); raise
