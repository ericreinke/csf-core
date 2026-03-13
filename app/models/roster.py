import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.models.league import generate_uuid7


class Roster(Base):
    __tablename__ = "roster"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=generate_uuid7)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    tag: Mapped[str | None] = mapped_column(String(10), nullable=True)
    league_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("league.id"), nullable=False)
    league: Mapped["League"] = relationship("League")
    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("user.id"), nullable=False)
    owner: Mapped["User"] = relationship("User")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
