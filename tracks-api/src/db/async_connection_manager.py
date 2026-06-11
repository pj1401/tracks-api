"""
AsyncDatabaseConnectionManager class.
module: src/db/async_connection_manager.py
"""

from typing import AsyncGenerator, TypeVar
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from models import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)


class AsyncDatabaseConnectionManager:
    """
    Manage SQLAlchemy async sessions.
    """

    async def __init__(self, db_uri: str, base_model: type[TModel]):
        """
        Initialise the engine.
        """
        self.engine = create_async_engine(db_uri, pool_pre_ping=True)
        self.async_session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )
        await self._create_tables(base_model)

    async def _create_tables(self, base_model: type[TModel]) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(base_model.metadata.create_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_factory() as session:
            yield session
