"""
The WritableRepository class.
module: src/services/writable_repo.py
"""

from typing import Any, Dict, Generic, TypeVar
from sqlalchemy import select, update
from pydantic import BaseModel as PydanticBaseModel
from src.repositories.base_repo import BaseRepository
from src.util.error import NotFoundError
from models.filters import BaseFilters
from models import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)
TFilters = TypeVar("TFilters", bound=BaseFilters)
TArgs = TypeVar("TArgs", bound=PydanticBaseModel)


class WritableRepository(
    BaseRepository[TModel, TFilters], Generic[TModel, TFilters, TArgs]
):
    """
    Data-access layer for the read/write collections.
    """

    async def post(self, arguments: TArgs) -> Dict[str, Any]:
        """
        Create a new resource.

        :param arguments: The arguments object.
        :type arguments: Type[TSchema]
        :return: A dictionary representing the newly created resource.
        :rtype: Dict[str, Any]
        """
        try:
            resource = self.get_new_model(arguments)
            self.session.add(resource)
            await self.session.commit()
            await self.session.refresh(resource)
            return self.model_to_dict(resource)
        except Exception:
            await self.session.rollback()
            raise

    def get_new_model(self, arguments: TArgs) -> TModel:
        """
        Map the arguments for the database model.

        :param arguments: The arguments object.
        :type arguments: Type[TSchema]
        """
        return self.model()

    async def update(self, id: int, arguments: TArgs):
        """
        Update a resource.

        :param id: The id of the resource.
        :type id: int
        :param arguments: The arguments object.
        :type arguments: TArgs
        """
        try:
            stmt = self._get_update_stmt(id, arguments)
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    def _get_update_stmt(self, id: int, arguments: TArgs):
        """
        Get the statement for updating the resource.

        :param id: The id of the resource.
        :type id: int
        :param arguments: The arguments object.
        :type arguments: TArgs
        :return: The update statement.
        :rtype: Update
        """
        return (
            update(self.model).where(self.model.id == id).values(arguments.model_dump())
        )

    async def delete(self, id: int):
        """
        Delete a resource.

        :param id: The id of the resource.
        :type id: int
        """
        try:
            stmt = select(self.model).where(self.model.id == id)
            result = self.session.scalars(stmt).first()
            if result is None:
                raise NotFoundError()
            await self.session.delete(result)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
