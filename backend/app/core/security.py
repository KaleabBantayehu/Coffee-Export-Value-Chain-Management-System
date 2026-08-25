import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt


def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_jwt_token(subject: str, role: str, secret_key: str, expires_delta_minutes: int) -> tuple[str, datetime]:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_delta_minutes)
    payload = {
        "sub": subject,
        "role": role,
        "exp": int(expires_at.timestamp()),
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token, expires_at
