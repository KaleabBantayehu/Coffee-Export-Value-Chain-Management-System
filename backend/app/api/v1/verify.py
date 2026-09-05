from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import ErrorResponse
from app.schemas.lot import QRVerificationResponse
from app.services import qr_service

router = APIRouter(prefix="/verify", tags=["qr"])


@router.get(
    "/{qr_id}",
    response_model=QRVerificationResponse,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
async def verify_qr(
    qr_id: int = Path(..., gt=0),
    sig: str = Query(..., min_length=1),
    session: Session = Depends(get_db),
) -> QRVerificationResponse:
    try:
        return qr_service.verify_qr(
            session,
            qr_id=qr_id,
            supplied_signature=sig,
        )
    except qr_service.QRVerificationInvalidError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from None
    except qr_service.QRVerificationNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from None
