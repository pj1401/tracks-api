"""
The ArtistRepository class.
module: src/repositories/artist_repo.py
"""

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
