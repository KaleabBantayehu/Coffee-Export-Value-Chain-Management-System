import json

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.identifiers import generate_farmer_fin
from app.db.models import AuditLog, Cooperative, Farmer


class FarmerServiceError(Exception):
    pass


class DuplicateNationalIdError(FarmerServiceError):
    pass


class CooperativeNotFoundError(FarmerServiceError):
    pass


class FarmerNotFoundError(FarmerServiceError):
    pass


def _normalize_text(value: str) -> str:
    return value.strip()


def _validate_cooperative(session: Session, cooperative_id: int | None) -> None:
    if cooperative_id is None:
        return
    exists = session.query(Cooperative).filter(Cooperative.cooperative_id == cooperative_id).one_or_none()
    if exists is None:
        raise CooperativeNotFoundError(f"Cooperative {cooperative_id} not found.")


def create_farmer(
    session: Session,
    *,
    full_name: str,
    national_id: str,
    gender: str,
    phone_number: str,
    cooperative_id: int | None,
) -> Farmer:
    full_name = _normalize_text(full_name)
    national_id = _normalize_text(national_id)
    gender = _normalize_text(gender)
    phone_number = _normalize_text(phone_number)

    _validate_cooperative(session, cooperative_id)
    if session.query(Farmer).filter(Farmer.national_id == national_id).one_or_none() is not None:
        raise DuplicateNationalIdError("National ID already exists.")

    farmer = Farmer(
        fin_code=generate_farmer_fin(session),
        full_name=full_name,
        national_id=national_id,
        gender=gender,
        phone_number=phone_number,
        cooperative_id=cooperative_id,
    )
    session.add(farmer)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        if session.query(Farmer).filter(Farmer.national_id == national_id).one_or_none() is not None:
            raise DuplicateNationalIdError("National ID already exists.") from None
        raise
    session.refresh(farmer)
    return farmer


def get_farmer(session: Session, farmer_id: int) -> Farmer:
    farmer = session.query(Farmer).filter(Farmer.farmer_id == farmer_id).one_or_none()
    if farmer is None:
        raise FarmerNotFoundError(f"Farmer {farmer_id} not found.")
    return farmer


def update_farmer(
    session: Session,
    *,
    farmer_id: int,
    full_name: str,
    national_id: str,
    gender: str,
    phone_number: str,
    cooperative_id: int | None,
    acting_user_id: int,
) -> Farmer:
    farmer = get_farmer(session, farmer_id)
    _validate_cooperative(session, cooperative_id)

    if national_id != farmer.national_id and session.query(Farmer).filter(Farmer.national_id == national_id).one_or_none() is not None:
        raise DuplicateNationalIdError("National ID already exists.")

    previous_state = {
        "full_name": farmer.full_name,
        "national_id": farmer.national_id,
        "gender": farmer.gender,
        "phone_number": farmer.phone_number,
        "cooperative_id": farmer.cooperative_id,
    }

    farmer.full_name = _normalize_text(full_name)
    farmer.national_id = _normalize_text(national_id)
    farmer.gender = _normalize_text(gender)
    farmer.phone_number = _normalize_text(phone_number)
    farmer.cooperative_id = cooperative_id

    session.add(
        AuditLog(
            user_id=acting_user_id,
            action="update_farmer",
            entity_type="Farmer",
            entity_id=farmer.farmer_id,
            old_value=json.dumps(previous_state, sort_keys=True),
            new_value=json.dumps(
                {
                    "full_name": farmer.full_name,
                    "national_id": farmer.national_id,
                    "gender": farmer.gender,
                    "phone_number": farmer.phone_number,
                    "cooperative_id": farmer.cooperative_id,
                },
                sort_keys=True,
            ),
        )
    )
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        if session.query(Farmer).filter(Farmer.national_id == farmer.national_id).filter(Farmer.farmer_id != farmer_id).one_or_none() is not None:
            raise DuplicateNationalIdError("National ID already exists.") from None
        raise
    session.refresh(farmer)
    return farmer


def search_farmers(session: Session, search: str | None) -> list[Farmer]:
    query = session.query(Farmer)
    if search is None or not search.strip():
        return query.order_by(Farmer.farmer_id).all()

    term = f"%{search.strip()}%"
    query = query.outerjoin(Cooperative, Farmer.cooperative_id == Cooperative.cooperative_id).filter(
        or_(Farmer.fin_code.ilike(term), Farmer.full_name.ilike(term), Cooperative.name.ilike(term))
    )
    return query.order_by(Farmer.farmer_id).all()
