import uuid

from sqlalchemy import ForeignKey, UUID, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.league import generate_uuid7
from app.models.player import Player
from app.models.map import Map


class GameStats(Base):
    __tablename__ = "game_stats"

    id: Mapped[uuid.UUID] = mapped_column(
        "uuid", primary_key=True, default=generate_uuid7
    )
    
    player_uuid: Mapped[uuid.UUID | None] = mapped_column(UUID, ForeignKey("player.uuid", ondelete="CASCADE"), nullable=True)
    player: Mapped["Player"] = relationship("Player")
    
    map_uuid: Mapped[uuid.UUID | None] = mapped_column(UUID, ForeignKey("map.uuid", ondelete="CASCADE"), nullable=True)
    map_: Mapped["Map"] = relationship("Map")
    
    stats: Mapped[dict] = mapped_column(JSONB, nullable=False)

    __table_args__ = (
        UniqueConstraint("player_uuid", "map_uuid", name="uq_game_stats_player_map"),
    )
