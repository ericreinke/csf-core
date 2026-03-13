import uuid
import enum

from sqlalchemy import String, Integer, Text, ForeignKey, Enum, UUID, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.league import generate_uuid7
from app.models.tournament import Tournament
from app.models.team import Team


class DemoDownloadStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Match(Base):
    __tablename__ = "match"

    id: Mapped[uuid.UUID] = mapped_column(
        "uuid", primary_key=True, default=generate_uuid7
    )
    hltv_id: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)
    hltv_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    demo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    demo_status: Mapped[DemoDownloadStatus] = mapped_column(
        Enum(DemoDownloadStatus, name="demo_download_status"), 
        default=DemoDownloadStatus.PENDING, 
        nullable=False
    )
    demo_retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    maximum_maps: Mapped[int] = mapped_column(Integer, default=3, nullable=False)

    tournament_uuid: Mapped[uuid.UUID | None] = mapped_column(UUID, ForeignKey("tournament.uuid", ondelete="CASCADE"), nullable=True)
    tournament: Mapped["Tournament"] = relationship("Tournament")
    
    team_a_uuid: Mapped[uuid.UUID | None] = mapped_column(UUID, ForeignKey("team.uuid"), nullable=True)
    team_a: Mapped["Team"] = relationship("Team", foreign_keys=[team_a_uuid])
    
    team_b_uuid: Mapped[uuid.UUID | None] = mapped_column(UUID, ForeignKey("team.uuid"), nullable=True)
    team_b: Mapped["Team"] = relationship("Team", foreign_keys=[team_b_uuid])

    __table_args__ = (
        Index(
            "idx_match_demo_pending",
            "demo_status",
            postgresql_where=(demo_status.in_(["PENDING", "FAILED"]))
        ),
    )
