import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.league import generate_uuid7


class RosterPlayer(Base):
    __tablename__ = "roster_player"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=generate_uuid7
    )
    roster_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roster.id", ondelete="CASCADE"), nullable=False
    )
    player_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("player.uuid", ondelete="CASCADE"), nullable=False
    )
    drafted_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    roster: Mapped["Roster"] = relationship("Roster", back_populates="players")
    player: Mapped["Player"] = relationship("Player")

    __table_args__ = (
        UniqueConstraint("roster_id", "player_id", name="uq_roster_player"),
    )
