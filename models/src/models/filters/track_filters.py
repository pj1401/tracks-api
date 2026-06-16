"""
The TrackFilters dataclass.
module: models.filters.track_filters
"""

from dataclasses import dataclass
from .base_filters import BaseFilters


@dataclass
class TrackFilters(BaseFilters):
    name: str | None = None
    artist: str | None = None
    album: str | None = None
    genre: str | None = None
    year: int | None = None
    mode: int | None = None
    min_total_playcount: int | None = None
    max_total_playcount: int | None = None
    tags: str | None = None
    artist_id: int | None = None
    album_id: int | None = None
