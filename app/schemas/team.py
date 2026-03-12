from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TeamCreate(BaseModel):
    """Request body for creating a team."""
    name: str
    tag: str | None = None
    league_id: UUID
    owner_id: UUID


class TeamUpdate(BaseModel):
    """Request body for updating a team. All fields optional — only provided fields are updated."""
    name: str | None = None
    tag: str | None = None


class TeamResponse(BaseModel):
    """Response body returned to the client. Mirrors the full DB model."""
    id: UUID
    name: str
    tag: str | None
    league_id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
