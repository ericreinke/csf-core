from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TournamentBase(BaseModel):
    title: str
    hltv_id: Optional[int] = None
    hltv_url: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class TournamentCreate(TournamentBase):
    """Fields provided when creating a tournament."""
    id: Optional[UUID] = None


class TournamentUpdate(BaseModel):
    """All fields optional for partial updates."""
    title: Optional[str] = None
    hltv_id: Optional[int] = None
    hltv_url: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class TournamentResponse(TournamentBase):
    id: UUID

    model_config = {"from_attributes": True}
