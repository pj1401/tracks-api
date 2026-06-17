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

    :var base_url: The base URL of the application.
    :vartype base_url: str
    :var path: The path to the collection. e.g. "/api/v1/tracks"
    :vartype path: str
    :var params: A Pydantic model containing the query parameter data.
    :vartype params: BaseQueryParams
    :var status: A HTTP status code.
    :vartype status: int
    :var data: A list of dictionaries representing the records.
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
            # Next is null if the number of returned records are less than limit.
            # Less than limit indicates the last page, so there is no next page.
            "next": self._build_url(offset + limit)
            if len(self.data) == limit
            else None,
            # Previous is null if offset is 0. If offset is 0, that indicates first page.
            "previous": self._build_url(max(offset - limit, 0)) if offset > 0 else None,
            "data": self.data,
        }
