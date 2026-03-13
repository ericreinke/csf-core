import uuid
import enum

from sqlalchemy import String, Integer, Text, ForeignKey, Enum, UUID, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.league import generate_uuid7
from app.models.match import Match


class DemoParsedStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Map(Base):
    __tablename__ = "map"

    id: Mapped[uuid.UUID] = mapped_column(
        "uuid", primary_key=True, default=generate_uuid7
    )
    hltv_id: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)
    hltv_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    match_uuid: Mapped[uuid.UUID | None] = mapped_column(UUID, ForeignKey("match.uuid", ondelete="CASCADE"), nullable=True)
    match: Mapped["Match"] = relationship("Match")
    
    map_name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    demo_parsed_status: Mapped[DemoParsedStatus] = mapped_column(
        Enum(DemoParsedStatus, name="demo_parsed_status"), 
        default=DemoParsedStatus.PENDING, 
        nullable=False
    )
    demo_parse_retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    __table_args__ = (
        Index(
            "idx_map_demo_parse_pending",
            "demo_parsed_status",
            postgresql_where=(demo_parsed_status.in_(["PENDING", "FAILED"]))
        ),
    )
