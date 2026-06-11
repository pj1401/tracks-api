from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.async_connection_manager import AsyncDatabaseConnectionManager


_db_manager: AsyncDatabaseConnectionManager | None = None


def init_db_manager(manager: AsyncDatabaseConnectionManager) -> None:
    global _db_manager
    _db_manager = manager


def get_db_manager() -> AsyncDatabaseConnectionManager:
    if _db_manager is None:
        raise RuntimeError("Database not initialised")
    return _db_manager


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_manager().get_session():
        yield session
