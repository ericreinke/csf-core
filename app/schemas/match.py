from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.match import DemoDownloadStatus


class MatchBase(BaseModel):
    hltv_id: Optional[int] = None
    hltv_url: Optional[str] = None
    demo_url: Optional[str] = None
    demo_status: DemoDownloadStatus = DemoDownloadStatus.PENDING
    demo_retry_count: int = 0
    maximum_maps: int = 3
    tournament_uuid: Optional[UUID] = None
    team_a_uuid: Optional[UUID] = None
    team_b_uuid: Optional[UUID] = None


class MatchCreate(MatchBase):
    """Fields provided when creating a match."""
    id: Optional[UUID] = None


class MatchUpdate(BaseModel):
    """All fields optional for partial updates."""
    hltv_id: Optional[int] = None
    hltv_url: Optional[str] = None
    demo_url: Optional[str] = None
    demo_status: Optional[DemoDownloadStatus] = None
    demo_retry_count: Optional[int] = None
    maximum_maps: Optional[int] = None
    tournament_uuid: Optional[UUID] = None
    team_a_uuid: Optional[UUID] = None
    team_b_uuid: Optional[UUID] = None


class MatchResponse(MatchBase):
    id: UUID

    model_config = {"from_attributes": True}
