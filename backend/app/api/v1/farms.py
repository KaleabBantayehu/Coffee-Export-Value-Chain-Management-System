from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.auth import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import ErrorResponse
from app.schemas.farm import FarmCreateRequest, FarmResponse
from app.services import farm_service

router = APIRouter(prefix="/farms", tags=["farms"])


def require_farm_management(user: User = Depends(get_current_user)) -> User:
    if user.role.role_name not in {"Admin", "Field/Registry Agent"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized.")
    return user


def _response(farm, geometry: dict) -> FarmResponse:
    return FarmResponse(
        farm_id=farm.farm_id,
        farmer_id=farm.farmer_id,
        geometry=geometry,
        area_hectares=farm.area_hectares,
        eudr_risk_flag=farm.eudr_risk_flag,
        created_at=farm.created_at,
    )


@router.post("", response_model=FarmResponse, status_code=status.HTTP_201_CREATED, responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}})
async def create_farm(
    body: FarmCreateRequest,
    _: User = Depends(require_farm_management),
    session: Session = Depends(get_db),
) -> FarmResponse:
    try:
        farm = farm_service.create_farm(
            session,
            farmer_id=body.farmer_id,
            geometry=body.geometry,
            radius_meters=body.radius_meters,
        )
        _, geometry = farm_service.get_farm(session, farm.farm_id)
    except farm_service.FarmerNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from None
    except farm_service.InvalidGeometryError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from None
    return _response(farm, geometry)


@router.get("/{farm_id}", response_model=FarmResponse, responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}})
async def get_farm(
    farm_id: int,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> FarmResponse:
    try:
        farm, geometry = farm_service.get_farm(session, farm_id)
    except farm_service.FarmNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farm not found.") from None
    return _response(farm, geometry)
