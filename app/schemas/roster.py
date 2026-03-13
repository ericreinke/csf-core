from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RosterCreate(BaseModel):
    """Request body for creating a roster."""
    name: str
    tag: str | None = None
    league_id: UUID
    owner_id: UUID


class RosterUpdate(BaseModel):
    """Request body for updating a roster. All fields optional — only provided fields are updated."""
    name: str | None = None
    tag: str | None = None


class RosterResponse(BaseModel):
    """Response body returned to the client. Mirrors the full DB model."""
    id: UUID
    name: str
    tag: str | None
    league_id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
