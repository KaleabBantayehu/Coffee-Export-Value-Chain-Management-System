from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.v1.lots import require_lot_management
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import ErrorResponse
from app.schemas.lot import QRGenerationRequest, QRGenerationResponse
from app.services import qr_service

router = APIRouter(prefix="/lots", tags=["qr"])


@router.post("/{lot_id}/qr", response_model=QRGenerationResponse, responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def generate_qr(lot_id: int, body: QRGenerationRequest, response: Response, _: User = Depends(require_lot_management), session: Session = Depends(get_db)) -> QRGenerationResponse:
    try:
        result, created = qr_service.generate_qr(session, lot_id=lot_id, regenerate=body.regenerate)
        response.status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return result
    except qr_service.QRLotNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from None
    except qr_service.QRConfigurationError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from None
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="QR generation failed.") from None
