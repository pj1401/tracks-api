"""
The starting point of the API.
module: src/main.py
"""

from fastapi import FastAPI
from models import BaseModel
from .routers.api.api_router import api_router
from .db.async_connection_manager import AsyncDatabaseConnectionManager
from .config import DbConfig, Settings


def create_app() -> FastAPI:
    app = FastAPI(title="Tracks API")
    settings = get_settings()
    init_db_connection(app, settings)
    include_routers(app)
    return app


def get_settings() -> Settings:
    """
    Get the Settings object containing the environment variables.

    :return: The Settings object.
    :rtype: Settings
    """
    return Settings()


def init_db_connection(app: FastAPI, settings: Settings) -> None:
    db_config = DbConfig(
        settings.db_host,
        settings.db_port,
        settings.db_name,
        settings.db_user,
        settings.db_password,
    )
    db_manager = AsyncDatabaseConnectionManager(db_config.uri, BaseModel)


def include_routers(app: FastAPI) -> None:
    app.include_router(api_router, prefix="/api")


app = create_app()
