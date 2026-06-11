"""
The TrackService class.
module: src/services/track_service.py
"""

from typing import Type
from src.services.writable_service import WritableService
from pydantic import BaseModel
from models.schemas import BaseQueryParams, BaseResourceSchema
from src.repositories.track_repo import TrackRepository


class TrackService(WritableService[TrackRepository, BaseQueryParams, BaseModel]):
    def __init__(
        self,
        track_repo: TrackRepository,
        track_schema: Type[BaseResourceSchema],
    ):
        super().__init__(track_repo, track_schema)
