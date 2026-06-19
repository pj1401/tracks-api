"""
AlbumQueryParams schema for filtering.
module: src.models.schemas.albums.album_query_params
"""

from .. import BaseQueryParams


class AlbumQueryParams(BaseQueryParams):
    name: str | None = None
