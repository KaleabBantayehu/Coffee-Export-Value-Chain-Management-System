from pydantic import BaseModel, Field

from app.schemas.auth import UserProfileResponse


class UserCreateRequest(BaseModel):
    """Admin-supplied payload for creating a new user account (AUTH-005).

    ``role`` is a role *name* (e.g. "Admin"), validated against the seeded
    roles in the service layer. No password-strength policy is enforced here:
    Design Document §8 specifies only "validates unique username; hashes
    password before storage" for V1.0, so only presence is validated at this
    boundary.
    """

    username: str = Field(..., min_length=1, max_length=128)
    password: str = Field(..., min_length=1)
    full_name: str = Field(..., min_length=1, max_length=256)
    role: str = Field(..., min_length=1)


class UserRoleUpdateRequest(BaseModel):
    """Payload for ``PATCH /users/{id}/role`` — the new role name."""

    role: str = Field(..., min_length=1)


class PaginatedUsersResponse(BaseModel):
    """Page envelope for ``GET /users`` (Design Document §8: "Supports
    pagination.").

    ``items`` never carries password material — it reuses
    :class:`UserProfileResponse`, whose fields are id/username/full_name/role.
    """

    items: list[UserProfileResponse]
    total: int
    page: int
    page_size: int
