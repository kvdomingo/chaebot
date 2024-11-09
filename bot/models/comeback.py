from django.db import models
from ulid import ULID


def ulid_factory() -> str:
    return str(ULID())


class Comeback(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        db_index=True,
        null=False,
        default=ulid_factory,
    )
    date = models.DateTimeField(db_index=True)
    artist = models.TextField(db_index=True)
    album_title = models.TextField()
    release = models.TextField(null=True, blank=True)
    song_title = models.TextField(null=True, blank=True)
    album_type = models.TextField(null=True, blank=True)
    title_track = models.TextField(null=True, blank=True)
    artist_type = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"[{self.date}] {self.artist} - {self.album_title}"
