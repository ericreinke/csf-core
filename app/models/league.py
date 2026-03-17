import uuid
from datetime import datetime

from uuid_utils import uuid7


def generate_uuid7() -> uuid.UUID:
    """Generate a UUID v7 and return it as a standard uuid.UUID for psycopg2 compatibility."""
    return uuid.UUID(str(uuid7()))

from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
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

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=generate_uuid7)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[LeagueStatus] = mapped_column(
        Enum(LeagueStatus), nullable=False, default=LeagueStatus.OPEN
    )
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("account.id"), nullable=False)
    owner: Mapped["Account"] = relationship("Account")
    pools: Mapped[list["LeaguePool"]] = relationship("LeaguePool", back_populates="league")
    pool_size: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    registration_deadline: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    draft_start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    league_length: Mapped[int | None] = mapped_column(Integer, nullable=True)
    prize_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
