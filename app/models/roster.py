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
    
    pool_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("league_pool.uuid", ondelete="CASCADE"), nullable=False)
    pool: Mapped["LeaguePool"] = relationship("LeaguePool", back_populates="rosters")
    
    registration_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("league_registration.uuid"), nullable=False)

    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("account.id"), nullable=False)
    owner: Mapped["Account"] = relationship("Account")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
