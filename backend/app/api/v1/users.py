from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1.auth import require_permissions
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import ErrorResponse, UserProfileResponse
from app.schemas.user import (
    PaginatedUsersResponse,
    UserCreateRequest,
    UserRoleUpdateRequest,
)
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])

# Every route below is Admin-only, enforced by reusing AUTH-004's RBAC
# mechanism (the "users:manage" permission is seeded only for Admin). No ad hoc
# role check is re-implemented here.
_require_user_management = require_permissions("users:manage")


def _to_profile(user: User) -> UserProfileResponse:
    return UserProfileResponse(
        user_id=user.user_id,
        username=user.username,
        full_name=user.full_name,
        role=user.role.role_name,
    )


@router.get(
    "",
    response_model=PaginatedUsersResponse,
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    _admin: User = Depends(_require_user_management),
    session: Session = Depends(get_db),
) -> PaginatedUsersResponse:
    """List users (Admin only), paginated by ``page``/``page_size``."""
    users, total = user_service.list_users(session, page=page, page_size=page_size)
    return PaginatedUsersResponse(
        items=[_to_profile(user) for user in users],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post(
    "",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def create_user(
    body: UserCreateRequest,
    _admin: User = Depends(_require_user_management),
    session: Session = Depends(get_db),
) -> UserProfileResponse:
    """Create a user account (Admin only). Password is hashed before storage."""
    try:
        user = user_service.create_user(
            session,
            username=body.username,
            password=body.password,
            full_name=body.full_name,
            role_name=body.role,
        )
    except user_service.InvalidRoleError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role.") from None
    except user_service.DuplicateUsernameError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists."
        ) from None
    return _to_profile(user)


@router.patch(
    "/{user_id}/role",
    response_model=UserProfileResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def change_user_role(
    user_id: int,
    body: UserRoleUpdateRequest,
    admin: User = Depends(_require_user_management),
    session: Session = Depends(get_db),
) -> UserProfileResponse:
    """Change a user's role (Admin only) and write an AuditLog entry."""
    try:
        user = user_service.change_user_role(
            session,
            target_user_id=user_id,
            new_role_name=body.role,
            acting_admin_id=admin.user_id,
        )
    except user_service.UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.") from None
    except user_service.InvalidRoleError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role.") from None
    return _to_profile(user)
