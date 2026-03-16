from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RosterPlayerCreate(BaseModel):
    player_id: UUID


class RosterPlayerResponse(BaseModel):
    id: UUID
    roster_id: UUID
    player_id: UUID
    drafted_at: datetime

    model_config = {"from_attributes": True}
