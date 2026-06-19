"""
ArtistQueryParams schema for filtering.
module: src.models.schemas.artists.artist_query_params
"""

from .. import BaseQueryParams


class ArtistQueryParams(BaseQueryParams):
    name: str | None = None
