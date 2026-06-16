"""
The PaginatedResponse dataclass.
module: src.util.paginated_response
"""

from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode
from models.schemas import BaseQueryParams


@dataclass
class PaginatedResponse:
    """
    Used to build pagination links.
    """

    base_url: str
    path: str
    params: BaseQueryParams
    status: int
    data: list[Any]

    def _build_url(self, offset: int) -> str:
        """Build the URL using the parameters from the Pydantic model."""
        query = self.params.model_dump(exclude_none=True)
        query["offset"] = offset
        return f"{self.base_url}{self.path}?{urlencode(query)}"

    def to_dict(self) -> dict[str, int | str | Any]:
        """Get a dictionary representation of the paginated response."""
        offset = self.params.offset
        limit = self.params.limit
        return {
            "status": self.status,
            "href": self._build_url(offset),
            "next": self._build_url(offset + limit)
            if len(self.data) == limit
            else None,
            "previous": self._build_url(max(offset - limit, 0)) if offset > 0 else None,
            "data": self.data,
        }
