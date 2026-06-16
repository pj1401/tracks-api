"""
The PaginatedResponse dataclass.
module: src.util.paginated_response
"""

from dataclasses import dataclass
from typing import Any
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
