from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class PlayerBase(BaseModel):
    hltv_id: Optional[int] = None
    steam_id: Optional[int] = None
    user_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    country: Optional[str] = None
    profile_photo_url: Optional[str] = None


class PlayerCreate(PlayerBase):
    """Fields provided when creating a player (UUID can be explicitly set by scraper)."""
    id: Optional[UUID] = None


class PlayerUpdate(PlayerBase):
    """Fields a player can update."""
    pass


class PlayerResponse(PlayerBase):
    """Player data returned in API responses."""
    id: UUID

    model_config = {"from_attributes": True}
