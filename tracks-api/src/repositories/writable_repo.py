"""
The WritableRepository class.
module: src/services/writable_repo.py
"""

from typing import Any, Dict, Generic, TypeVar
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from pydantic import BaseModel as PydanticBaseModel
from src.repositories.base_repo import BaseRepository
from src.util.errors.error import NotFoundError
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

    def post(self, arguments: TArgs) -> Dict[str, Any]:
        """
        Create a new resource.

        :param arguments: The arguments object.
        :type arguments: Type[TSchema]
        :return: A dictionary representing the newly created resource.
        :rtype: Dict[str, Any]
        """
        session: Session | None = None
        try:
            session = self.db_manager.get_session()
            resource = self.get_new_model(arguments)
            session.add(resource)
            session.commit()
            session.refresh(resource)
            dict = self.model_to_dict(resource)
            return dict
        except Exception as err:
            if session is not None:
                session.rollback()
            raise err
        finally:
            if session is not None:
                session.close()

    def get_new_model(self, arguments: TArgs) -> TModel:
        """
        Map the arguments for the database model.

        :param arguments: The arguments object.
        :type arguments: Type[TSchema]
        """
        return self.model()

    def update(self, id: int, arguments: TArgs):
        """
        Update a resource.

        :param id: The id of the resource.
        :type id: int
        :param arguments: The arguments object.
        :type arguments: TArgs
        """
        session: Session | None = None
        try:
            session = self.db_manager.get_session()
            stmt = self._get_update_stmt(id, arguments)
            session.execute(stmt)
            session.commit()
        except Exception as err:
            if session is not None:
                session.rollback()
            raise err
        finally:
            if session is not None:
                session.close()

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

    def delete(self, id: int):
        """
        Delete a resource.

        :param id: The id of the resource.
        :type id: int
        """
        session: Session | None = None
        try:
            session = self.db_manager.get_session()
            stmt = select(self.model).where(self.model.id == id)
            result = session.scalars(stmt).first()
            if result is None:
                raise NotFoundError()
            session.delete(result)
            session.commit()
        except Exception as err:
            if session is not None:
                session.rollback()
            raise err
        finally:
            if session is not None:
                session.close()
