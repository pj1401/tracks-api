"""
The BaseRepository class.
module: src/repositories/base_repo.py
"""

from typing import Any, Dict, Generic, TypeVar
from sqlalchemy import Select, select
from sqlalchemy.orm import Session
from src.util.filters.base_filters import BaseFilters
from src.db.connection_manager import DatabaseConnectionManager
from src.util.errors.error import NotFoundError
from src.util.models.base import BaseModel

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
        self, db_manager: DatabaseConnectionManager, model: type[TModel], base_url: str
    ) -> None:
        """
        Initialise the repository with a database connection manager.

        :param db_manager: Provides scoped SQLAlchemy sessions backed by
            the application's configured database engine.
        :type db_manager: DatabaseConnectionManager
        :param model: The SQLAlchemy model used for data-access.
        :type model: type[TModel]
        :param base_url: The base URL of the application.
        :type base_url: str
        """
        self.db_manager = db_manager
        self.model = model
        self.base_url = base_url

    def get(self, filters: TFilters) -> list[Dict[str, Any]]:
        """
        Get a list of records by using filters to match the result.

        :param filters: The query parameters that have been converted to a BaseFilters like dataclass.
        :type filters: TFilters
        :return: A list of dictionaries representing the records.
        :rtype: list[Dict[str, Any]]
        """
        session: Session | None = None
        try:
            session = self.db_manager.get_session()
            stmt = self._get_stmt(filters)
            result = session.scalars(stmt.offset(filters.offset)).fetchmany(
                filters.limit
            )
            dicts = [self.model_to_dict(row) for row in result]
            session.commit()
            return dicts
        except Exception as err:
            if session is not None:
                session.rollback()
            raise err
        finally:
            if session is not None:
                session.close()

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

    def get_by_id(self, id: int | str) -> Dict[str, Any]:
        """
        Fetch one record by matching ID.

        :param id: The id of the record.
        :type id: int | str
        :return: The dictionary representing the record if a match is found.
        :rtype: Dict[str, Any]
        """
        session: Session | None = None
        try:
            session = self.db_manager.get_session()
            stmt = select(self.model).where(self.model.id == id)
            result = session.scalars(stmt).first()
            if result is None:
                raise NotFoundError()

            # Get a dictionary representing the fetched record.
            dict = self.model_to_dict(result)

            session.commit()
            return dict
        except Exception as err:
            if session is not None:
                session.rollback()
            raise err
        finally:
            if session is not None:
                session.close()

    def model_to_dict(self, model: TModel) -> Dict[str, Any]:
        """
        Get a dictionary representing the model.

        :param model: The model for the object.
        :type model: TModel
        :return: A dictionary representing the model.
        :rtype: Dict[str, Any]
        """
        return model.to_dict()
