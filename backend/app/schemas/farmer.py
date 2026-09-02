from datetime import datetime

from pydantic import BaseModel, Field


class FarmerCreateRequest(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=256)
    national_id: str = Field(..., min_length=1, max_length=128)
    gender: str = Field(..., min_length=1, max_length=32)
    phone_number: str = Field(..., min_length=1, max_length=64)
    cooperative_id: int | None = None


class FarmerUpdateRequest(FarmerCreateRequest):
    pass


class FarmerResponse(BaseModel):
    farmer_id: int
    fin_code: str
    full_name: str
    national_id: str
    gender: str | None = None
    phone_number: str | None = None
    cooperative_id: int | None = None
    created_at: datetime


class FarmerDetailResponse(FarmerResponse):
    linked_farms: list[dict] = Field(default_factory=list)
    farms: list[dict] = Field(default_factory=list)
