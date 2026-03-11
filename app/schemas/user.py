from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Fields provided when a user signs up via Google OAuth."""
    google_id: str
    email: str
    display_name: str
    avatar_url: str | None = None


class UserUpdate(BaseModel):
    """Fields a user can update on their profile."""
    display_name: str | None = None
    avatar_url: str | None = None


class UserResponse(BaseModel):
    """User data returned in API responses."""
    id: UUID
    google_id: str
    email: str
    display_name: str
    avatar_url: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
