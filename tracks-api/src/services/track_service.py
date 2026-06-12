"""
The TrackService class.
module: src/services/track_service.py
"""

from typing import Type
from src.services.writable_service import WritableService
from models.schemas.tracks import TrackParams, TrackQueryParams, TrackSchema
from src.repositories.track_repo import TrackRepository


class TrackService(WritableService[TrackRepository, TrackQueryParams, TrackParams]):
    def __init__(
        self,
        track_repo: TrackRepository,
        track_schema: Type[TrackSchema],
    ):
        super().__init__(track_repo, track_schema)
