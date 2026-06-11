"""
The BaseService class.
module: src/services/base_service.py
"""

from typing import Any, Dict, Generic, Type, TypeVar
from pydantic import BaseModel as PydanticBaseModel
from src.util.errors.error import ForbiddenError
from models.filters import BaseFilters
from models.schemas import BaseQueryParams
from src.repositories.base_repo import BaseRepository

TRepository = TypeVar("TRepository", bound=BaseRepository[Any, Any])
TSchema = TypeVar("TSchema", bound=PydanticBaseModel)
TQueryParams = TypeVar("TQueryParams", bound=BaseQueryParams)


class BaseService(Generic[TRepository, TQueryParams]):
    """
    BaseService encapsulates business logic.
    """

    def __init__(self, repository: TRepository, schema: Type[TSchema]):
        """
        Initialise the service with its repository dependency.

        :param repository: Repository used for data-access.
        :type repository: TRepository
        :param schema: The schema that is used for data validation.
        :type schema: Type[TSchema]
        """
        self.repository = repository
        self.schema = schema

    def get(self, params: TQueryParams) -> list[Dict[str, Any]]:
        """
        Get a list of records using optional query parameters.

        :param params: The query parameters.
        :type params: TQueryParams
        :return: A list of dictionaries representing the records.
        :rtype: list[Dict[str, Any]]
        """
        try:
            filters = self._get_filters(params)
            results = self.repository.get(filters)
            return [self.schema.model_validate(item).model_dump() for item in results]
        except Exception as err:
            raise err

    def _get_filters(self, params: TQueryParams) -> BaseFilters:
        """
        Convert query parameters to filters.

        :param params: The query parameters structured like a BaseQueryParams object.
        :type params: TQueryParams
        :return: The BaseFilters or similar object.
        :rtype: BaseFilters
        """
        return BaseFilters(
            limit=params.limit,
            offset=params.offset,
        )

    def get_by_id(self, id: int | str) -> Dict[str, Any]:
        """
        Fetch one record's data by matching ID.

        :param id: The id of the record.
        :type id: int | str
        :return: A dictionary representing the record data.
        :rtype: Dict[str, Any]
        """
        try:
            data = self.repository.get_by_id(id)
            return self.schema.model_validate(data).model_dump()
        except Exception as err:
            raise err

    def authorize(self, user_id: int, current_user_id: int) -> None:
        """
        Check if the user is the owner of a resource.

        :param user_id: The user ID from the resource.
        :type user_id: int
        :param current_user_id: The user ID from the JWT.
        :type current_user_id: int
        """
        if user_id != current_user_id:
            raise ForbiddenError()
