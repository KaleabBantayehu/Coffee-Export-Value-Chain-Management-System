from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.farm import FarmResponse
from app.schemas.farmer import FarmerResponse


class CoffeeLotCreateRequest(BaseModel):
    farm_id: int = Field(..., gt=0)


class CoffeeLotResponse(BaseModel):
    lot_id: int
    gin_code: str
    farm_id: int
    created_by: int
    status: str
    created_at: datetime


class TraceabilityEventCreateRequest(BaseModel):
    event_type: str = Field(..., min_length=1, max_length=128)
    notes: str | None = Field(default=None)


class TraceabilityEventResponse(BaseModel):
    event_id: int
    lot_id: int
    event_type: str
    event_timestamp: datetime
    recorded_by: int
    notes: str | None = None


class LotTraceResponse(BaseModel):
    lot: CoffeeLotResponse
    farm: FarmResponse
    farmer: FarmerResponse
    events: list[TraceabilityEventResponse]


class QRGenerationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    regenerate: bool = False


class QRGenerationResponse(BaseModel):
    qr_id: int
    verification_url: str
    image_svg: str
    image_png_data_url: str
