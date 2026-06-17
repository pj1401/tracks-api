"""
The BaseRepository class.
module: src/repositories/base_repo.py
"""

from typing import Any, Dict, Generic, TypeVar
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.filters import BaseFilters
from src.util.error import NotFoundError
from models import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)
TFilters = TypeVar("TFilters", bound=BaseFilters)


class BaseRepository(Generic[TModel, TFilters]):
    """
    Data-access layer.

    Encapsulates all SQLAlchemy interactions so that the rest
    of the application can work with plain domain objects without dealing
    with sessions, transactions or ORM-specific exceptions.
    """

    def __init__(
        self,
        session: AsyncSession,
        model: type[TModel],
        base_url: str,
        collections_path: str,
    ) -> None:
        """
        Initialise the repository.

        :param session: The session used for the database transaction.
        :type session: AsyncSession
        :param model: The SQLAlchemy model used for data-access.
        :type model: type[TModel]
        :param base_url: The base URL of the application.
        :type base_url: str
        :param collections_path: The path to the collections. e.g. "/api/v1"
        :type collections_path: str
        """
        self.session = session
        self.model = model
        self.base_url = base_url
        self.collections_path = collections_path

    async def get(self, filters: TFilters) -> list[Dict[str, Any]]:
        """
        Get a list of records by using filters to match the result.

        :param filters: The query parameters that have been converted to a BaseFilters like dataclass.
        :type filters: TFilters
        :return: A list of dictionaries representing the records.
        :rtype: list[Dict[str, Any]]
        """
        try:
            stmt = self._get_stmt(filters)
            result = await self.session.scalars(stmt.offset(filters.offset))
            rows = result.fetchmany(filters.limit)
            return [self.model_to_dict(row) for row in rows]
        except Exception:
            await self.session.rollback()
            raise

    def _get_stmt(self, filters: TFilters) -> Select[Any]:
        """
        Get the statement for the collection query.

        :param filters: The BaseFilters or similar object.
        :type filters: TFilters
        :return: The statement using filters if any.
        :rtype: Select[Any]
        """
        return select(self.model)

    def _get_filtered_stmt(self, stmt: Select[Any], filters: TFilters) -> Select[Any]:
        """
        Get a statement using the filters.

        :param stmt: The base statement.
        :type stmt: Select[Any]
        :param filters: The filters object.
        :type filters: TFilters
        :return: The statement using filters.
        :rtype: Select[Any]
        """
        return stmt

    async def get_by_id(self, id: int | str) -> Dict[str, Any]:
        """
        Fetch one record by matching ID.

        :param id: The id of the record.
        :type id: int | str
        :return: The dictionary representing the record if a match is found.
        :rtype: Dict[str, Any]
        """
        try:
            stmt = self._get_by_id_stmt(id)
            result = (await self.session.scalars(stmt)).first()
            if result is None:
                raise NotFoundError()

            # Return a dictionary representing the fetched record.
            return self.model_to_dict(result)
        except Exception:
            await self.session.rollback()
            raise

    def _get_by_id_stmt(self, id: int | str) -> Select[Any]:
        """
        Get the statement for fetching a record by ID.

        :return: The statement using the ID to find the record.
        :rtype: Select[Any]
        """
        return select(self.model).where(self.model.id == id)

    def model_to_dict(self, model: TModel) -> Dict[str, Any]:
        """
        Get a dictionary representing the model.

        :param model: The model for the object.
        :type model: TModel
        :return: A dictionary representing the model.
        :rtype: Dict[str, Any]
        """
        return model.to_dict()
