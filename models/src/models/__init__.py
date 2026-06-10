# type: ignore
# ruff: disable[F401]
from .album import Album
from .artist import Artist, artists_tracks_table, artists_albums_table
from .base import BaseModel
from .track import Track, tracks_albums_table
from .user import User

__all__ = [
    "Album",
    "Artist",
    "BaseModel",
    "Track",
    "User",
    "artists_tracks_table",
    "artists_albums_table",
    "tracks_albums_table",
]
