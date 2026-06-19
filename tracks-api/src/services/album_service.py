"""
The AlbumService class.
module: src/services/album_service.py
"""

from typing import Type
from models.filters import AlbumFilters
from models.schemas.albums import AlbumSchema, AlbumQueryParams
from src.repositories.album_repo import AlbumRepository
from src.services.base_service import BaseService


class AlbumService(BaseService[AlbumRepository, AlbumQueryParams]):
    """
    AlbumService encapsulates business logic for the album collection.
    """

    def __init__(self, album_repo: AlbumRepository, album_schema: Type[AlbumSchema]):
        super().__init__(album_repo, album_schema)

    def _get_filters(self, params: AlbumQueryParams) -> AlbumFilters:
        return AlbumFilters(
            limit=params.limit,
            offset=params.offset,
            sort=params.sort,
            name=params.name,
        )
