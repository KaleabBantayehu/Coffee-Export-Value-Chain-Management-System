from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.auth import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import ErrorResponse
from app.schemas.farm import FarmResponse
from app.schemas.farmer import FarmerResponse
from app.schemas.lot import CoffeeLotCreateRequest, CoffeeLotResponse, LotTraceResponse, TraceabilityEventCreateRequest, TraceabilityEventResponse
from app.services import farm_service, lot_service

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


@router.post("/{lot_id}/events", response_model=TraceabilityEventResponse, status_code=status.HTTP_201_CREATED, responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}})
async def append_traceability_event(lot_id: int, body: TraceabilityEventCreateRequest, acting_user: User = Depends(get_current_user), session: Session = Depends(get_db)) -> TraceabilityEventResponse:
    try:
        return lot_service.append_traceability_event(session, lot_id=lot_id, event_type=body.event_type, notes=body.notes, recorded_by=acting_user.user_id)
    except lot_service.CoffeeLotNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from None


@router.get("/{lot_id}/trace", response_model=LotTraceResponse, responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}})
async def get_lot_trace(
    lot_id: int,
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> LotTraceResponse:
    try:
        lot, farm, farmer, events = lot_service.get_lot_trace(session, lot_id=lot_id)
        _, geometry = farm_service.get_farm(session, farm.farm_id)
    except lot_service.CoffeeLotNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from None

    return LotTraceResponse(
        lot=CoffeeLotResponse(
            lot_id=lot.lot_id,
            gin_code=lot.gin_code,
            farm_id=lot.farm_id,
            created_by=lot.created_by,
            status=lot.status,
            created_at=lot.created_at,
        ),
        farm=FarmResponse(
            farm_id=farm.farm_id,
            farmer_id=farm.farmer_id,
            geometry=geometry,
            area_hectares=farm.area_hectares,
            eudr_risk_flag=farm.eudr_risk_flag,
            created_at=farm.created_at,
        ),
        farmer=FarmerResponse(
            farmer_id=farmer.farmer_id,
            fin_code=farmer.fin_code,
            full_name=farmer.full_name,
            national_id=farmer.national_id,
            gender=farmer.gender,
            phone_number=farmer.phone_number,
            cooperative_id=farmer.cooperative_id,
            created_at=farmer.created_at,
        ),
        events=[
            TraceabilityEventResponse(
                event_id=event.event_id,
                lot_id=event.lot_id,
                event_type=event.event_type,
                event_timestamp=event.event_timestamp,
                recorded_by=event.recorded_by,
                notes=event.notes,
            )
            for event in events
        ],
    )
