import uuid

from sqlalchemy import String, Integer, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.league import generate_uuid7
from app.models.league import League


class LeaguePool(Base):
    __tablename__ = "league_pool"

    id: Mapped[uuid.UUID] = mapped_column(
        "uuid", primary_key=True, default=generate_uuid7
    )
    
    league_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("league.id", ondelete="CASCADE"), nullable=False)
    league: Mapped["League"] = relationship("League", back_populates="pools")
    
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    max_teams: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    
    rosters: Mapped[list["Roster"]] = relationship("Roster", back_populates="pool")
