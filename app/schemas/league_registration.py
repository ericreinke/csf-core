from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from app.models.league_registration import RegistrationStatus


class LeagueRegistrationBase(BaseModel):
    pass


class LeagueRegistrationCreate(LeagueRegistrationBase):
    """Fields provided when an account registers for a league."""
    account_id: UUID
    # league_id is inferred from the path param


class LeagueRegistrationResponse(LeagueRegistrationBase):
    """Registration data returned in API responses."""
    id: UUID
    account_id: UUID
    league_id: UUID
    pool_id: Optional[UUID] = None
    status: RegistrationStatus
    created_at: datetime

    model_config = {"from_attributes": True}
