"""
The TrackRepository class.
module: src/repositories/track_repo.py
"""

from typing import Any, Dict
from sqlalchemy import Select, func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.writable_repo import WritableRepository
from models import Album, Artist, Track
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
        stmt = select(Track).options(
            selectinload(Track.artists), selectinload(Track.albums)
        )
        return self._get_filtered_stmt(stmt, filters)

    def _get_filtered_stmt(
        self, stmt: Select[Any], filters: TrackFilters
    ) -> Select[Any]:
        if filters.album:
            stmt = self._get_album_filtered_stmt(stmt, filters.album)
        if filters.album_id:
            stmt = self._get_album_id_filtered_stmt(stmt, filters.album_id)
        if filters.artist:
            stmt = self._get_artist_filtered_stmt(stmt, filters.artist)
        if filters.artist_id:
            stmt = self._get_artist_id_filtered_stmt(stmt, filters.artist_id)
        if filters.genre:
            stmt = self._get_genre_filtered_stmt(stmt, filters.genre)
        if filters.min_total_playcount:
            stmt = self._get_min_total_playcount_filtered_stmt(
                stmt, filters.min_total_playcount
            )
        if filters.max_total_playcount:
            stmt = self._get_max_total_playcount_filtered_stmt(
                stmt, filters.max_total_playcount
            )
        if filters.mode:
            stmt = self._get_mode_filtered_stmt(stmt, filters.mode)
        if filters.name:
            stmt = self._get_name_filtered_stmt(stmt, filters.name)
        if filters.tags:
            stmt = self._get_tags_filtered_stmt(stmt, filters.tags)
        if filters.year:
            stmt = self._get_year_filtered_stmt(stmt, filters.year)

        return stmt

    def _get_album_filtered_stmt(self, stmt: Select[Any], album: str) -> Select[Any]:
        return stmt.where(
            Track.albums.any(func.lower(Album.name).contains(album.lower()))
        )

    def _get_album_id_filtered_stmt(
        self, stmt: Select[Any], album_id: int
    ) -> Select[Any]:
        return stmt.where(Track.albums.any(Album.id == album_id))

    def _get_artist_filtered_stmt(self, stmt: Select[Any], artist: str) -> Select[Any]:
        return stmt.where(
            Track.artists.any(func.lower(Artist.name).contains(artist.lower()))
        )

    def _get_artist_id_filtered_stmt(
        self, stmt: Select[Any], artist_id: int
    ) -> Select[Any]:
        return stmt.where(Track.artists.any(Artist.id == artist_id))

    def _get_genre_filtered_stmt(self, stmt: Select[Any], genre: str) -> Select[Any]:
        return stmt.where(func.lower(Track.genre) == func.lower(genre))

    def _get_min_total_playcount_filtered_stmt(
        self, stmt: Select[Any], min_total_playcount: int
    ) -> Select[Any]:
        return stmt.where(Track.total_playcount >= min_total_playcount)

    def _get_max_total_playcount_filtered_stmt(
        self, stmt: Select[Any], max_total_playcount: int
    ) -> Select[Any]:
        return stmt.where(Track.total_playcount <= max_total_playcount)

    def _get_mode_filtered_stmt(self, stmt: Select[Any], mode: int) -> Select[Any]:
        return stmt.where(Track.mode == mode)

    def _get_name_filtered_stmt(self, stmt: Select[Any], name: str) -> Select[Any]:
        return stmt.where(func.lower(Track.name).contains(name.lower()))

    def _get_tags_filtered_stmt(self, stmt: Select[Any], tags: str) -> Select[Any]:
        return stmt.where(func.lower(Track.tags).contains(tags.lower()))

    def _get_year_filtered_stmt(self, stmt: Select[Any], year: int) -> Select[Any]:
        return stmt.where(Track.year == year)

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
