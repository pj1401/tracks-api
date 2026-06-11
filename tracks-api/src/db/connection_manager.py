"""
DatabaseConnectionManager class.
module: src/db/connection_manager.py
"""

from typing import TypeVar
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)


class DatabaseConnectionManager:
    def __init__(self, db_uri: str, base_model: type[TModel]):
        """
        Initialise the engine.
        """
        self.engine = create_engine(db_uri.uri, pool_pre_ping=True)
        base_model.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self.session_factory()
