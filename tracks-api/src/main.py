"""
The starting point of the API.
module: src/main.py
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from functools import lru_cache
from fastapi import FastAPI
from models import BaseModel
from .routers.api.api_router import api_router
from .db.async_connection_manager import AsyncDatabaseConnectionManager
from .config import DbConfig, Settings


@lru_cache
def get_settings() -> Settings:
    """
    Get the Settings object containing the environment variables.

    :return: The Settings object.
    :rtype: Settings
    """
    return Settings()


_db_manager: AsyncDatabaseConnectionManager | None = None


def get_db_manager() -> AsyncDatabaseConnectionManager:
    if _db_manager is None:
        raise RuntimeError("Database not initialised")
    return _db_manager


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_manager().get_session():
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Define startup and shutdown logic.
    """
    settings = get_settings()
    db_config = DbConfig(
        settings.db_host,
        settings.db_port,
        settings.db_name,
        settings.db_user,
        settings.db_password,
    )
    _db_manager = AsyncDatabaseConnectionManager(db_config.uri, BaseModel)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Tracks API", lifespan=lifespan)
    include_routers(app)
    return app


def include_routers(app: FastAPI) -> None:
    app.include_router(api_router, prefix="/api")


app = create_app()
