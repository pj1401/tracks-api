"""
The TrackRepository class.
module: src/repositories/track_repo.py
"""

from typing import Any, Dict
from sqlalchemy import Select, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.writable_repo import WritableRepository
from models import Track
from models.filters import TrackFilters
from models.schemas.tracks import TrackParams


class TrackRepository(WritableRepository[Track, TrackFilters, TrackParams]):
    """
    Data-access layer for the tracks collection.
    """

    def __init__(
        self,
        session: AsyncSession,
        track_model: type[Track],
        base_url: str,
    ):
        super().__init__(session, track_model, base_url)

    def _get_stmt(self, filters: TrackFilters) -> Select[Any]:
        return select(Track).options(
            selectinload(Track.artists), selectinload(Track.albums)
        )

    def _get_by_id_stmt(self, id: int | str) -> Select[Any]:
        return (
            select(Track)
            .where(Track.id == id)
            .options(selectinload(Track.artists), selectinload(Track.albums))
        )

    def model_to_dict(self, model: Track) -> Dict[str, Any]:
        data = model.to_dict()
        data["href"] = f"{self.base_url}/api/v1/tracks/{model.id}"
        data["artists"] = [
            {
                "id": a.id,
                "href": f"{self.base_url}/api/v1/artists/{a.id}",
            }
            for a in model.artists
        ]
        data["albums"] = [
            {
                "id": a.id,
                "href": f"{self.base_url}/api/v1/albums/{a.id}",
            }
            for a in model.albums
        ]
        return data
