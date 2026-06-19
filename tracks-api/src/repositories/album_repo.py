"""
The AlbumRepository class.
module: src/repositories/album_repo.py
"""

from typing import Any, Dict
from sqlalchemy import Select, func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repo import BaseRepository
from models import Album
from models.filters import AlbumFilters


class AlbumRepository(BaseRepository[Album, AlbumFilters]):
    """
    Data-access layer for the album collection.
    """

    def __init__(
        self,
        session: AsyncSession,
        album_model: type[Album],
        base_url: str,
        collections_path: str,
    ):
        super().__init__(session, album_model, base_url, collections_path)

    def _get_stmt(self, filters: AlbumFilters) -> Select[Any]:
        stmt = select(Album).options(
            selectinload(Album.tracks), selectinload(Album.artists)
        )
        return self._get_filtered_stmt(stmt, filters)

    def _get_filtered_stmt(
        self, stmt: Select[Any], filters: AlbumFilters
    ) -> Select[Any]:
        if filters.name:
            stmt = self._get_name_filtered_stmt(stmt, filters.name)

        return stmt

    def _get_name_filtered_stmt(self, stmt: Select[Any], name: str) -> Select[Any]:
        return stmt.where(func.lower(Album.name).contains(name.lower()))

    def _get_by_id_stmt(self, id: int | str) -> Select[Any]:
        return (
            select(Album)
            .where(Album.id == id)
            .options(selectinload(Album.tracks), selectinload(Album.artists))
        )

    def model_to_dict(self, model: Album) -> Dict[str, Any]:
        data = model.to_dict()
        data["href"] = f"{self.base_url}{self.collections_path}/albums/{model.id}"
        data["tracks"] = (
            f"{self.base_url}{self.collections_path}/tracks?album_id={model.id}"
        )
        data["artists"] = [
            {
                "id": a.id,
                "href": f"{self.base_url}{self.collections_path}/artists/{a.id}",
            }
            for a in model.artists
        ]
        return data
