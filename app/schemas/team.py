from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TeamBase(BaseModel):
    hltv_id: Optional[int] = None
    name: str


class TeamCreate(TeamBase):
    """Fields provided when creating a team."""
    id: Optional[UUID] = None


class TeamUpdate(BaseModel):
    """All fields optional for partial updates."""
    hltv_id: Optional[int] = None
    name: Optional[str] = None


class TeamResponse(TeamBase):
    id: UUID

    model_config = {"from_attributes": True}
