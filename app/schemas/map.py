from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.map import DemoParsedStatus


class MapBase(BaseModel):
    hltv_id: Optional[int] = None
    hltv_url: Optional[str] = None
    match_uuid: Optional[UUID] = None
    map_name: str
    demo_parsed_status: DemoParsedStatus = DemoParsedStatus.PENDING
    demo_parse_retry_count: int = 0


class MapCreate(MapBase):
    """Fields provided when creating a map."""
    id: Optional[UUID] = None


class MapUpdate(BaseModel):
    """All fields optional for partial updates."""
    hltv_id: Optional[int] = None
    hltv_url: Optional[str] = None
    match_uuid: Optional[UUID] = None
    map_name: Optional[str] = None
    demo_parsed_status: Optional[DemoParsedStatus] = None
    demo_parse_retry_count: Optional[int] = None


class MapResponse(MapBase):
    id: UUID

    model_config = {"from_attributes": True}
