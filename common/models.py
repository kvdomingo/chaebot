from datetime import datetime

from sqlalchemy import TIMESTAMP, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    id: Mapped[str] = mapped_column(
        VARCHAR(26),
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )


class Comeback(BaseModel):
    __tablename__ = "comebacks"

    date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), index=True, nullable=False
    )
    artist: Mapped[str] = mapped_column(index=True, nullable=False)
    album_title: Mapped[str] = mapped_column(nullable=False)
    release: Mapped[str] = mapped_column()
    song_title: Mapped[str] = mapped_column()
    album_type: Mapped[str] = mapped_column()
    title_track: Mapped[str] = mapped_column()
    artist_type: Mapped[str] = mapped_column()
