from datetime import datetime

from uuid_utils import uuid7

from sqlalchemy import String, DateTime, Enum, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
import enum

from app.db.base import Base


class LeagueStatus(enum.Enum):
    """Tracks the lifecycle of a league."""
    OPEN = "open"            # League created, joinable
    ACTIVE = "active"        # Season in progress
    COMPLETED = "completed"  # Season finished


class League(Base):
    __tablename__ = "league"

    id: Mapped[uuid7] = mapped_column(Uuid, primary_key=True, default=uuid7)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[LeagueStatus] = mapped_column(
        Enum(LeagueStatus), nullable=False, default=LeagueStatus.OPEN
    )
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    owner: Mapped[str] = mapped_column(String(100), nullable=False)
    max_teams: Mapped[int] = mapped_column(nullable=False, default=8)
    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    league_length: Mapped[int | None] = mapped_column(Integer, nullable=True)
    prize_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
