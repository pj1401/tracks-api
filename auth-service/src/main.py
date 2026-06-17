"""
The starting point of the API.
module: src/main.py
"""

from typing import cast
from flask import Flask
from flask_jwt_extended import JWTManager
from models import BaseModel
from src.config.reverse_proxied import ReverseProxied
from src.config.logger_config import configure_logger
from src.decorators.logging import setup_logging_decorators
from src.decorators.exception_handlers import setup_exception_handlers
from src.decorators.database import setup_database_decorators
from src.config.db_config import DbConfig
from src.db.connection_manager import DatabaseConnectionManager
from src.config.load_config import load_config
from src.blueprints.router import router_bp


def create_app() -> Flask:
    """
    Set up the application.
    Flask application factory template: https://github.com/cookiecutter-flask/cookiecutter-flask/blob/master/%7B%7Bcookiecutter.app_name%7D%7D/%7B%7Bcookiecutter.app_name%7D%7D/app.py

    :return: The Flask app.
    :rtype: Flask
    """
    # https://github.com/cookiecutter-flask/cookiecutter-flask/blob/master/%7B%7Bcookiecutter.app_name%7D%7D/%7B%7Bcookiecutter.app_name%7D%7D/app.py
    app = Flask(__name__, static_folder="../static")
    load_config(app)
    register_db_manager(app)
    register_reverse_proxy(app)
    register_blueprints(app)
    register_exception_handlers(app)
    init_jwt_manager(app)
    set_up_logger(app)

    return app


def register_db_manager(app: Flask) -> None:
    """Register a database manager."""
    db_manager = DatabaseConnectionManager(
        DbConfig(
            cast(str, app.config["DB_HOST"]),
            cast(int, app.config["DB_PORT"]),
            cast(str, app.config["DB_NAME"]),
            cast(str, app.config["DB_USER"]),
            cast(str, app.config["DB_PASSWORD"]),
        ),
        BaseModel,
    )
    setup_database_decorators(app, db_manager)


def register_reverse_proxy(app: Flask):
    app.wsgi_app = ReverseProxied(app.wsgi_app)  # type: ignore


def register_blueprints(app: Flask) -> None:
    """Register Flask blueprints."""
    app.register_blueprint(router_bp)


def register_exception_handlers(app: Flask) -> None:
    """Register exception handlers."""
    setup_exception_handlers(app)


def init_jwt_manager(app: Flask) -> None:
    """Initialise JWT manager."""
    jwt = JWTManager(app)  # type: ignore  # noqa: F841


def set_up_logger(app: Flask) -> None:
    """Configure logger and set up logging decorators."""
    configure_logger(app)
    setup_logging_decorators(app)


if __name__ == "__main__":
    app = create_app()
    host = cast(str, app.config["FLASK_HOST"])
    app.run(host=host)

app = create_app()
