from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.identifiers import generate_coffee_lot_gin
from app.db.models import CoffeeLot, Farm, Farmer, TraceabilityEvent


class CoffeeLotServiceError(Exception):
    pass


class FarmNotFoundError(CoffeeLotServiceError):
    pass


class GinGenerationError(CoffeeLotServiceError):
    pass


class CoffeeLotNotFoundError(CoffeeLotServiceError):
    pass


def create_coffee_lot(session: Session, *, farm_id: int, created_by: int) -> CoffeeLot:
    """Persist a Lot and its required initial event in one transaction."""
    try:
        farm = session.query(Farm).filter(Farm.farm_id == farm_id).one_or_none()
        if farm is None:
            raise FarmNotFoundError(f"Farm {farm_id} not found.")

        try:
            gin_code = generate_coffee_lot_gin(session)
        except ValueError as exc:
            raise GinGenerationError(str(exc)) from exc

        lot = CoffeeLot(
            gin_code=gin_code,
            farm_id=farm.farm_id,
            created_by=created_by,
            status="created",
        )
        session.add(lot)
        session.flush()
        session.add(
            TraceabilityEvent(
                lot_id=lot.lot_id,
                event_type="lot_created",
                event_timestamp=datetime.now(timezone.utc),
                recorded_by=created_by,
                notes=None,
            )
        )
        session.commit()
        session.refresh(lot)
        return lot
    except Exception:
        session.rollback()
        raise


def append_traceability_event(session: Session, *, lot_id: int, event_type: str, notes: str | None, recorded_by: int) -> TraceabilityEvent:
    if session.query(CoffeeLot).filter(CoffeeLot.lot_id == lot_id).one_or_none() is None:
        raise CoffeeLotNotFoundError(f"Coffee Lot {lot_id} not found.")
    event = TraceabilityEvent(lot_id=lot_id, event_type=event_type, event_timestamp=datetime.now(timezone.utc), recorded_by=recorded_by, notes=notes)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


def get_lot_trace(session: Session, *, lot_id: int) -> tuple[CoffeeLot, Farm, Farmer, list[TraceabilityEvent]]:
    """Retrieve the Lot origin in fixed queries, with events in chronological order."""
    origin = (
        session.query(CoffeeLot, Farm, Farmer)
        .join(Farm, CoffeeLot.farm_id == Farm.farm_id)
        .join(Farmer, Farm.farmer_id == Farmer.farmer_id)
        .filter(CoffeeLot.lot_id == lot_id)
        .one_or_none()
    )
    if origin is None:
        raise CoffeeLotNotFoundError(f"Coffee Lot {lot_id} not found.")

    lot, farm, farmer = origin
    events = (
        session.query(TraceabilityEvent)
        .filter(TraceabilityEvent.lot_id == lot.lot_id)
        .order_by(TraceabilityEvent.event_timestamp, TraceabilityEvent.event_id)
        .all()
    )
    return lot, farm, farmer, events
