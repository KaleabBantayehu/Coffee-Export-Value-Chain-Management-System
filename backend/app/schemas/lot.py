from datetime import datetime

from pydantic import BaseModel, Field


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
