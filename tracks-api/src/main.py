"""
The starting point of the API.
module: src/main.py
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from models import BaseModel
from .apis import api_v1
from .routers.router import router
from .db.async_connection_manager import AsyncDatabaseConnectionManager
from .config import DbConfig
from .dependencies import init_db_manager, get_settings


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
    db_manager = await AsyncDatabaseConnectionManager.create(db_config.uri, BaseModel)
    init_db_manager(db_manager)
    yield
    await db_manager.dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Tracks API", lifespan=lifespan, root_path=settings.root_path)
    include_routers(app)
    mount_versioned_apis(app)
    return app


def include_routers(app: FastAPI) -> None:
    app.include_router(router)


def mount_versioned_apis(app: FastAPI) -> None:
    """
    Mount versioned APIs as sub applications.

    :param app: The main FastAPI app.
    :type app: FastAPI
    """
    app.mount("/api/v1", api_v1)


app = create_app()
