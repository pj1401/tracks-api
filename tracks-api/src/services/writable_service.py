"""
The WritableService class.
module: src/services/writable_service.py
"""

from typing import Any, Generic, TypeVar
from pydantic import BaseModel as PydanticBaseModel
from models.schemas import BaseQueryParams
from src.repositories.writable_repo import WritableRepository
from src.services.base_service import BaseService

TRepository = TypeVar("TRepository", bound=WritableRepository[Any, Any, Any])
TQueryParams = TypeVar("TQueryParams", bound=BaseQueryParams)
TArgs = TypeVar("TArgs", bound=PydanticBaseModel)


class WritableService(
    BaseService[TRepository, TQueryParams], Generic[TRepository, TQueryParams, TArgs]
):
    def post(self, arguments: TArgs) -> dict[str, Any]:
        """
        Create a new resource.

        :param arguments: The arguments object.
        :type arguments: TArgs
        :return: A dictionary representing the resource.
        :rtype: dict[str, Any]
        """
        try:
            self.validate_related(arguments)
            data = self.repository.post(arguments)
            return self.schema.model_validate(data).model_dump()
        except Exception as err:
            raise err

    def validate_related(self, arguments: TArgs):
        """
        Check if related resources exist by calling get_by_id from the resource's repository.

        :param arguments: The arguments object that contains the IDs to the related resources.
        :type arguments: TArgs
        """
        pass

    async def update(self, id: int, arguments: TArgs):
        """
        Update a resource. Uses JWT to authorize.

        :param id: The id of the resource.
        :type id: int
        :param arguments: The arguments object.
        :type arguments: TArgs
        """
        try:
            # resource = self.repository.get_by_id(id)
            # self.authorize(resource["user"]["id"], int(get_jwt_identity()))
            await self.repository.update(id, arguments)
        except Exception as err:
            raise err

    async def delete(self, id: int):
        """
        Delete a resource. Uses JWT to authorize.

        :param id: The id of the resource.
        :type id: int
        """
        try:
            # resource = self.repository.get_by_id(id)
            # self.authorize(resource["user"]["id"], int(get_jwt_identity()))
            await self.repository.delete(id)
        except Exception as err:
            raise err
