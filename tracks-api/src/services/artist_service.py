"""
The ArtistService class.
module: src/services/artist_service.py
"""

from typing import Type
from models.filters import ArtistFilters
from models.schemas.artists import ArtistSchema, ArtistQueryParams
from src.repositories.artist_repo import ArtistRepository
from src.services.base_service import BaseService


class ArtistService(BaseService[ArtistRepository, ArtistQueryParams]):
    """
    ArtistService encapsulates business logic for the artist collection.
    """

    def __init__(
        self, artist_repo: ArtistRepository, artist_schema: Type[ArtistSchema]
    ):
        super().__init__(artist_repo, artist_schema)

    def _get_filters(self, params: ArtistQueryParams) -> ArtistFilters:
        return ArtistFilters(
            limit=params.limit,
            offset=params.offset,
            sort=params.sort,
            name=params.name,
        )
