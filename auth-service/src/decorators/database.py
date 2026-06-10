"""
Set up decorators related to the database.
module: src/decorators/database.py
"""

from flask import Flask, g
from src.db.connection_manager import DatabaseConnectionManager


def setup_database_decorators(
    app: Flask, db_manager: DatabaseConnectionManager
) -> None:
    """Add db_manager to the application context, so it can be accessed during a request."""

    @app.before_request
    def before_request() -> None:  # pyright: ignore[reportUnusedFunction]
        g.db_manager = db_manager
