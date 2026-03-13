from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class RosterBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    tag: str | None = Field(None, min_length=2, max_length=10)


class RosterCreate(RosterBase):
    """Request body for creating a roster (must be tied to a specific registration)."""
    registration_id: UUID
    owner_id: UUID


class RosterUpdate(BaseModel):
    """Request body for updating a roster."""
    name: str | None = None
    tag: str | None = None


class RosterResponse(RosterBase):
    """Response body returned to the client."""
    id: UUID
    pool_id: UUID
    registration_id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
