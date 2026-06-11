"""
The starting point of the API.
module: src/main.py
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from models import BaseModel
from .routers.api.api_router import api_router
from .db.async_connection_manager import AsyncDatabaseConnectionManager
from .config import DbConfig
from .dependencies import get_settings
import src.dependencies.db as db_deps


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
    db_deps._db_manager = await AsyncDatabaseConnectionManager.create(
        db_config.uri, BaseModel
    )
    yield
    await db_deps._db_manager.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title="Tracks API", lifespan=lifespan)
    include_routers(app)
    return app


def include_routers(app: FastAPI) -> None:
    app.include_router(api_router, prefix="/api")


app = create_app()
