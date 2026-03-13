from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class LeaguePoolBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    max_teams: int = Field(10, ge=2, le=50)


class LeaguePoolCreate(LeaguePoolBase):
    """Fields provided when an admin or automated task creates a pool for a league."""
    league_id: UUID


class LeaguePoolUpdate(BaseModel):
    """Fields that can be updated after creation."""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    max_teams: Optional[int] = Field(None, ge=2, le=50)


class LeaguePoolResponse(LeaguePoolBase):
    """Pool data returned in API responses."""
    id: UUID
    league_id: UUID

    model_config = {"from_attributes": True}
