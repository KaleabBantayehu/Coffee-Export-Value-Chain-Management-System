import re
import secrets

from sqlalchemy.orm import Session

from app.db.models import Farmer


def _as_session(session: Session | object | None):
    """Accept either a SQLAlchemy Session or a Connection-like object."""
    if session is None:
        return None
    if hasattr(session, "query"):
        return session
    if hasattr(session, "bind"):
        return Session(bind=session.bind)
    if hasattr(session, "engine"):
        return Session(bind=session.engine)
    raise TypeError("Expected a SQLAlchemy Session or Connection-like object.")

FIN_PREFIX = "ETH-FAR-"
FIN_REGION_DIGIT_COUNT = 4
FIN_SEQUENCE_DIGIT_COUNT = 6
FIN_FORMAT_PATTERN = "ETH-FAR-XXXX-XXXXXX"
FIN_VALIDATOR = re.compile(r"^ETH-FAR-\d{4}-\d{6}$")


def format_farmer_fin(region_code: int | str, sequence_number: int | str) -> str:
    """Return the canonical CEVCMS V1.0 Farmer Identification Number."""
    region = str(region_code).zfill(FIN_REGION_DIGIT_COUNT)
    sequence = str(sequence_number).zfill(FIN_SEQUENCE_DIGIT_COUNT)
    return f"{FIN_PREFIX}{region}-{sequence}"


def validate_farmer_fin(fin_code: str | None) -> bool:
    """Return ``True`` when the supplied FIN matches the approved V1.0 pattern."""
    if not isinstance(fin_code, str):
        return False
    return bool(FIN_VALIDATOR.fullmatch(fin_code))


def generate_farmer_fin(session: Session | object | None = None, *, max_attempts: int = 20) -> str:
    """Generate a unique Farmer FIN.

    The canonical format is approved in the project decision for EPIC-2
    (`ETH-FAR-XXXX-XXXXXX`). The region segment is a four-digit zero-padded
    value and the trailing sequence is a six-digit zero-padded value.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    db_session = _as_session(session)
    created_new_session = db_session is not None and db_session is not session

    try:
        for _ in range(max_attempts):
            region_code = secrets.randbelow(10**FIN_REGION_DIGIT_COUNT)
            sequence_number = secrets.randbelow(10**FIN_SEQUENCE_DIGIT_COUNT)
            candidate = format_farmer_fin(region_code, sequence_number)

            if db_session is None:
                return candidate

            existing = db_session.query(Farmer).filter(Farmer.fin_code == candidate).first()
            if existing is None:
                return candidate

        raise ValueError(
            "Unable to generate a unique Farmer FIN within the allowed retry limit. "
            "Please retry or investigate the uniqueness constraint."
        )
    finally:
        if created_new_session:
            db_session.close()


__all__ = [
    "FIN_PREFIX",
    "FIN_REGION_DIGIT_COUNT",
    "FIN_SEQUENCE_DIGIT_COUNT",
    "FIN_FORMAT_PATTERN",
    "format_farmer_fin",
    "validate_farmer_fin",
    "generate_farmer_fin",
]
