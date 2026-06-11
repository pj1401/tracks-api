"""
The TrackRepository class.
module: src/repositories/track_repo.py
"""

from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.writable_repo import WritableRepository
from models import Track
from models.filters import BaseFilters
from pydantic import BaseModel


class TrackRepository(WritableRepository[Track, BaseFilters, BaseModel]):
    """
    Data-access layer for the tacks collection.
    """

    def __init__(
        self,
        session: AsyncSession,
        track_model: type[Track],
        base_url: str,
    ):
        super().__init__(session, track_model, base_url)

    def model_to_dict(self, model: Track) -> Dict[str, Any]:
        data = model.to_dict()
        data["href"] = f"{self.base_url}/api/v1/tracks/{model.id}"
        return data
