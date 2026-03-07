from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.league import LeagueStatus


class LeagueCreate(BaseModel):
    """Request body for creating a league. Only includes fields the client provides."""
    name: str
    description: str | None = None
    owner: str
    max_teams: int = 8
    start_time: datetime | None = None
    league_length: int | None = None
    prize_description: str | None = None


class LeagueUpdate(BaseModel):
    """Request body for updating a league. All fields optional — only provided fields are updated."""
    name: str | None = None
    description: str | None = None
    status: LeagueStatus | None = None
    max_teams: int | None = None
    start_time: datetime | None = None
    league_length: int | None = None
    prize_description: str | None = None


class LeagueResponse(BaseModel):
    """Response body returned to the client. Mirrors the full DB model."""
    id: UUID
    name: str
    status: LeagueStatus
    description: str | None
    owner: str
    max_teams: int
    start_time: datetime | None
    league_length: int | None
    prize_description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
