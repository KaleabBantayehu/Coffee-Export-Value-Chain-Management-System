from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.auth import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import ErrorResponse
from app.schemas.lot import CoffeeLotCreateRequest, CoffeeLotResponse
from app.services import lot_service

router = APIRouter(prefix="/lots", tags=["lots"])


def require_lot_management(user: User = Depends(get_current_user)) -> User:
    if user.role.role_name not in {"Admin", "Field/Registry Agent"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized.")
    return user


@router.post(
    "",
    response_model=CoffeeLotResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def create_coffee_lot(
    body: CoffeeLotCreateRequest,
    acting_user: User = Depends(require_lot_management),
    session: Session = Depends(get_db),
) -> CoffeeLotResponse:
    try:
        return lot_service.create_coffee_lot(
            session,
            farm_id=body.farm_id,
            created_by=acting_user.user_id,
        )
    except lot_service.FarmNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from None
    except lot_service.GinGenerationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from None
