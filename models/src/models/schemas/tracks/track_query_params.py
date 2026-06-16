"""
TrackQueryParams schema for filtering.
module: src.models.schemas.tracks.track_query_params
"""

from pydantic import Field
from .. import BaseQueryParams
from .track import Mode


class TrackQueryParams(BaseQueryParams):
    name: str | None = None
    artist: str | None = None
    album: str | None = None
    genre: str | None = None
    year: int | None = None
    mode: Mode | None = None
    min_total_playcount: int | None = Field(None, ge=0)
    max_total_playcount: int | None = Field(None, ge=0)
    tags: str | None = None
    artist_id: int | None = None
    album_id: int | None = None
