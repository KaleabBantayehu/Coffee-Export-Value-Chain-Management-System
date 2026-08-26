from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_jwt_token, decode_jwt_token, verify_password
from app.db.models import Permission, Role, User
from app.db.session import get_db
from app.schemas.auth import ErrorResponse, LoginRequest, LoginResponse, LogoutResponse, UserProfileResponse

router = APIRouter(prefix="/auth", tags=["auth"])

RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_ATTEMPTS = 5
_rate_limit_store: dict[str, dict[str, Any]] = {}


def _get_client_key(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _check_rate_limit(request: Request) -> None:
    key = _get_client_key(request)
    now = datetime.now(timezone.utc)
    entry = _rate_limit_store.get(key)

    if entry is None or now >= entry["reset_at"]:
        _rate_limit_store[key] = {
            "attempts": 1,
            "reset_at": now + timedelta(seconds=RATE_LIMIT_WINDOW_SECONDS),
        }
        return

    if entry["attempts"] >= RATE_LIMIT_MAX_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
        )

    entry["attempts"] += 1


def reset_rate_limit() -> None:
    _rate_limit_store.clear()


def _create_access_token(user_id: int, role: str) -> tuple[str, datetime]:
    settings = get_settings()
    token, expires_at = create_jwt_token(
        subject=str(user_id),
        role=role,
        secret_key=settings.JWT_SECRET_KEY,
        expires_delta_minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    return token, expires_at


def get_current_user(
    authorization: str | None = Header(default=None),
    session: Session = Depends(get_db),
) -> User:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_jwt_token(token.strip(), get_settings().JWT_SECRET_KEY)
        subject = payload.get("sub")
        role = payload.get("role")
        if not subject or not str(subject).isdigit() or not isinstance(role, str) or not role:
            raise JWTError("Invalid subject")
        user_id = int(subject)
    except (JWTError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    user = session.query(User).filter(User.user_id == user_id).one_or_none()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_permissions(*required_permissions: str):
    """Return a dependency that requires every named seeded permission."""
    required_permission_set = frozenset(required_permissions)

    def authorize(user: User = Depends(get_current_user), session: Session = Depends(get_db)) -> User:
        try:
            granted_permissions = {
                permission_code
                for (permission_code,) in (
                    session.query(Permission.permission_code)
                    .join(Permission.roles)
                    .filter(Role.role_id == user.role_id)
                    .all()
                )
            }
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized.",
            ) from None

        if not required_permission_set.issubset(granted_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized.",
            )
        return user

    return authorize


@router.post(
    "/login",
    response_model=LoginResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
    },
)
async def login(request: Request, body: LoginRequest, session: Session = Depends(get_db)) -> LoginResponse:
    _check_rate_limit(request)

    user = session.query(User).filter(User.username == body.username).one_or_none()
    if not user or not user.is_active or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    access_token, expires_at = _create_access_token(user.user_id, user.role.role_name)
    return LoginResponse(
        access_token=access_token,
        role=user.role.role_name,
        expires_at=expires_at,
    )


@router.get(
    "/me",
    response_model=UserProfileResponse,
    responses={401: {"model": ErrorResponse}},
)
async def get_authenticated_profile(user: User = Depends(get_current_user)) -> UserProfileResponse:
    return UserProfileResponse(
        user_id=user.user_id,
        username=user.username,
        full_name=user.full_name,
        role=user.role.role_name,
    )


@router.post(
    "/logout",
    response_model=LogoutResponse,
    responses={401: {"model": ErrorResponse}},
)
async def logout(_: User = Depends(get_current_user)) -> LogoutResponse:
    return LogoutResponse(detail="Logout acknowledged.")
