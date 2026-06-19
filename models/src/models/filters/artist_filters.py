"""
The ArtistFilters dataclass.
module: models.filters.artist_filters
"""

from dataclasses import dataclass
from .base_filters import BaseFilters


@dataclass
class ArtistFilters(BaseFilters):
    name: str | None = None
