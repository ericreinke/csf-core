from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class GameStatsBase(BaseModel):
    player_uuid: Optional[UUID] = None
    map_uuid: Optional[UUID] = None
    stats: dict[str, Any]


class GameStatsCreate(GameStatsBase):
    """Fields provided when creating game stats."""
    id: Optional[UUID] = None


class GameStatsUpdate(BaseModel):
    """All fields optional for partial updates."""
    player_uuid: Optional[UUID] = None
    map_uuid: Optional[UUID] = None
    stats: Optional[dict[str, Any]] = None


class GameStatsResponse(GameStatsBase):
    id: UUID

    model_config = {"from_attributes": True}
