"""
The TrackService class.
module: src/services/track_service.py
"""

from typing import Type
from src.services.writable_service import WritableService
from models.filters import TrackFilters
from models.schemas.tracks import TrackParams, TrackQueryParams, TrackSchema
from src.repositories.track_repo import TrackRepository


class TrackService(WritableService[TrackRepository, TrackQueryParams, TrackParams]):
    def __init__(
        self,
        track_repo: TrackRepository,
        track_schema: Type[TrackSchema],
    ):
        super().__init__(track_repo, track_schema)

    def _get_filters(self, params: TrackQueryParams) -> TrackFilters:
        return TrackFilters(
            limit=params.limit,
            offset=params.offset,
            name=params.name,
            artist=params.artist,
            album=params.album,
            genre=params.genre,
            year=params.year,
            mode=params.mode,
            min_total_playcount=params.min_total_playcount,
            max_total_playcount=params.max_total_playcount,
            artist_id=params.artist_id,
            album_id=params.album_id,
        )
