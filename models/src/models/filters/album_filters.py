"""
The AlbumFilters dataclass.
module: models.filters.album_filters
"""

from dataclasses import dataclass
from .base_filters import BaseFilters


@dataclass
class AlbumFilters(BaseFilters):
    name: str | None = None
