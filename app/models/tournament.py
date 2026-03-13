import uuid
from datetime import date

from sqlalchemy import String, Integer, Date, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.league import generate_uuid7


class Tournament(Base):
    __tablename__ = "tournament"

    id: Mapped[uuid.UUID] = mapped_column(
        "uuid", primary_key=True, default=generate_uuid7
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    hltv_id: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)
    hltv_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
