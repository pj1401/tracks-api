"""
The ArtistRepository class.
module: src/repositories/artist_repo.py
"""

from typing import Any, Dict
from sqlalchemy import Select, func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repo import BaseRepository
from models import Artist
from models.filters import ArtistFilters


class ArtistRepository(BaseRepository[Artist, ArtistFilters]):
    """
    Data-access layer for the artist collection.
    """

    def __init__(
        self,
        session: AsyncSession,
        artist_model: type[Artist],
        base_url: str,
        collections_path: str,
    ):
        super().__init__(session, artist_model, base_url, collections_path)

    def _get_stmt(self, filters: ArtistFilters) -> Select[Any]:
        stmt = select(Artist).options(
            selectinload(Artist.tracks), selectinload(Artist.albums)
        )
        return self._get_filtered_stmt(stmt, filters)

    def _get_filtered_stmt(
        self, stmt: Select[Any], filters: ArtistFilters
    ) -> Select[Any]:
        if filters.name:
            stmt = self._get_name_filtered_stmt(stmt, filters.name)

        return stmt

    def _get_name_filtered_stmt(self, stmt: Select[Any], name: str) -> Select[Any]:
        return stmt.where(func.lower(Artist.name).contains(name.lower()))

    def _get_by_id_stmt(self, id: int | str) -> Select[Any]:
        return (
            select(Artist)
            .where(Artist.id == id)
            .options(selectinload(Artist.tracks), selectinload(Artist.albums))
        )

    def model_to_dict(self, model: Artist) -> Dict[str, Any]:
        data = model.to_dict()
        data["href"] = f"{self.base_url}{self.collections_path}/artists/{model.id}"
        data["tracks"] = (
            f"{self.base_url}{self.collections_path}/tracks?artist_id={model.id}"
        )
        data["albums"] = [
            {
                "id": a.id,
                "href": f"{self.base_url}{self.collections_path}/albums/{a.id}",
            }
            for a in model.albums
        ]
        return data
