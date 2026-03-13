import uuid
import enum
from datetime import datetime

from sqlalchemy import String, ForeignKey, Enum, UUID, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.league import generate_uuid7
from app.models.league import League
from app.models.account import Account
from app.models.league_pool import LeaguePool


class RegistrationStatus(str, enum.Enum):
    REGISTERED = "REGISTERED"
    POOLED = "POOLED"
    DRAFTING = "DRAFTING"
    COMPLETED = "COMPLETED"


class LeagueRegistration(Base):
    __tablename__ = "league_registration"

    id: Mapped[uuid.UUID] = mapped_column(
        "uuid", primary_key=True, default=generate_uuid7
    )
    
    account_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("account.id"), nullable=False)
    account: Mapped["Account"] = relationship("Account")
    
    league_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("league.id", ondelete="CASCADE"), nullable=False)
    league: Mapped["League"] = relationship("League")
    
    pool_id: Mapped[uuid.UUID | None] = mapped_column(UUID, ForeignKey("league_pool.uuid"), nullable=True)
    pool: Mapped["LeaguePool"] = relationship("LeaguePool")
    
    status: Mapped[RegistrationStatus] = mapped_column(
        Enum(RegistrationStatus, name="registration_status"), 
        default=RegistrationStatus.REGISTERED, 
        nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # An account can only register for a specific league once
    __table_args__ = (
        UniqueConstraint("account_id", "league_id", name="uq_account_league_registration"),
    )
