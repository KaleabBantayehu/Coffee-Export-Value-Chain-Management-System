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
