from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.auth import require_permissions
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import ErrorResponse, UserProfileResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "",
    response_model=list[UserProfileResponse],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
async def list_users_for_authorization_proof(
    _: User = Depends(require_permissions("users:manage")),
    session: Session = Depends(get_db),
) -> list[UserProfileResponse]:
    """Minimal AUTH-004 proof route; AUTH-005 owns final user management."""
    users = session.query(User).order_by(User.user_id).all()
    return [
        UserProfileResponse(
            user_id=user.user_id,
            username=user.username,
            full_name=user.full_name,
            role=user.role.role_name,
        )
        for user in users
    ]
