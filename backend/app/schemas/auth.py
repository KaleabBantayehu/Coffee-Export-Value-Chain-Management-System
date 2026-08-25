from datetime import datetime

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    expires_at: datetime


class UserProfileResponse(BaseModel):
    user_id: int
    username: str
    full_name: str
    role: str


class LogoutResponse(BaseModel):
    detail: str


class ErrorResponse(BaseModel):
    detail: str
