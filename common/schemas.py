from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from ulid import ULID


class Comeback(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: ULID | None = Field(default_factory=ULID)
    date: datetime
    artist: str
    album_title: str
    release: str | None = Field(None)
    song_title: str | None = Field(None)
    album_type: str | None = Field(None)
    title_track: str | None = Field(None)
    artist_type: str | None = Field(None)
