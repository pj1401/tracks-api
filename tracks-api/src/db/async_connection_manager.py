"""
AsyncDatabaseConnectionManager class.
module: src/db/async_connection_manager.py
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from models import BaseModel


class AsyncDatabaseConnectionManager:
    """
    Manage SQLAlchemy async sessions.
    """

    def __init__(self, db_uri: str):
        """
        Initialise the engine.
        """
        self.engine = create_async_engine(db_uri, pool_pre_ping=True)
        self.async_session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )

    @classmethod
    async def create(
        cls, db_uri: str, base_model: type[BaseModel]
    ) -> "AsyncDatabaseConnectionManager":
        instance = cls(db_uri)
        await instance._create_tables(base_model)
        return instance

    async def _create_tables(self, base_model: type[BaseModel]) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(base_model.metadata.create_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_factory() as session:
            yield session

    async def dispose(self) -> None:
        """
        Dispose of the connection pool used by this engine.
        """
        await self.engine.dispose()
