from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.identifiers import generate_coffee_lot_gin
from app.db.models import CoffeeLot, Farm, TraceabilityEvent


class CoffeeLotServiceError(Exception):
    pass


class FarmNotFoundError(CoffeeLotServiceError):
    pass


class GinGenerationError(CoffeeLotServiceError):
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
