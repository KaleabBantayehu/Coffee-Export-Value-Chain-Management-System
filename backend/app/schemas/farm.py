from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class FarmCreateRequest(BaseModel):
    farmer_id: int = Field(..., gt=0)
    geometry: dict[str, Any]
    radius_meters: float | None = Field(default=None, gt=0)


class FarmResponse(BaseModel):
    farm_id: int
    farmer_id: int
    geometry: dict[str, Any]
    area_hectares: float | None = None
    eudr_risk_flag: bool | None = None
    eudr_check_type: str = "Demonstration review check (10-hectare area threshold; not EUDR compliance)."
    created_at: datetime
