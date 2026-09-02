from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.v1.auth import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import ErrorResponse
from app.schemas.farmer import FarmerCreateRequest, FarmerDetailResponse, FarmerResponse, FarmerUpdateRequest
from app.services import farmer_service

router = APIRouter(prefix="/farmers", tags=["farmers"])


def require_farmer_management(user: User = Depends(get_current_user)) -> User:
    if user.role.role_name not in {"Admin", "Field/Registry Agent"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )
    return user


@router.post(
    "",
    response_model=FarmerResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def create_farmer(
    body: FarmerCreateRequest,
    acting_user: User = Depends(require_farmer_management),
    session: Session = Depends(get_db),
) -> FarmerResponse:
    try:
        farmer = farmer_service.create_farmer(
            session,
            full_name=body.full_name,
            national_id=body.national_id,
            gender=body.gender,
            phone_number=body.phone_number,
            cooperative_id=body.cooperative_id,
        )
    except farmer_service.CooperativeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from None
    except farmer_service.DuplicateNationalIdError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from None
    return farmer


@router.get(
    "/{farmer_id}",
    response_model=FarmerDetailResponse,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def get_farmer(
    farmer_id: int,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> FarmerDetailResponse:
    try:
        farmer = farmer_service.get_farmer(session, farmer_id)
    except farmer_service.FarmerNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found.") from None
    detail = FarmerDetailResponse(
        farmer_id=farmer.farmer_id,
        fin_code=farmer.fin_code,
        full_name=farmer.full_name,
        national_id=farmer.national_id,
        gender=farmer.gender,
        phone_number=farmer.phone_number,
        cooperative_id=farmer.cooperative_id,
        created_at=farmer.created_at,
        linked_farms=[],
        farms=[],
    )
    return detail


@router.put(
    "/{farmer_id}",
    response_model=FarmerResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def update_farmer(
    farmer_id: int,
    body: FarmerUpdateRequest,
    acting_user: User = Depends(require_farmer_management),
    session: Session = Depends(get_db),
) -> FarmerResponse:
    try:
        farmer = farmer_service.update_farmer(
            session,
            farmer_id=farmer_id,
            full_name=body.full_name,
            national_id=body.national_id,
            gender=body.gender,
            phone_number=body.phone_number,
            cooperative_id=body.cooperative_id,
            acting_user_id=acting_user.user_id,
        )
    except farmer_service.FarmerNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farmer not found.") from None
    except farmer_service.CooperativeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from None
    except farmer_service.DuplicateNationalIdError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from None
    return farmer


@router.get(
    "",
    response_model=list[FarmerResponse],
    responses={
        401: {"model": ErrorResponse},
    },
)
async def search_farmers(
    search: str | None = Query(default=None, description="Search by FIN, name, or cooperative."),
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> list[FarmerResponse]:
    return farmer_service.search_farmers(session, search)
