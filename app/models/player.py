import uuid

from sqlalchemy import String, Integer, BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.league import generate_uuid7


class Player(Base):
    __tablename__ = "player"

    id: Mapped[uuid.UUID] = mapped_column(
        "uuid", primary_key=True, default=generate_uuid7
    )
    hltv_id: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)
    steam_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, nullable=True)
    user_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    profile_photo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
