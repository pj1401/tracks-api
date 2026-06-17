"""
Load env variables to a config object.
module: src/config/load_config.py
"""

import os
from dotenv import load_dotenv
from datetime import timedelta
from flask import Config, Flask

load_dotenv()


class TypedConfig(Config):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    FLASK_DEBUG: str
    FLASK_HOST: str
    SECRET_KEY: str
    JWT_PRIVATE_KEY: str
    JWT_PUBLIC_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRES: timedelta
    JWT_LEEWAY: timedelta
    BASE_URL: str
    PATH_PREFIX: str


def _get_env_or_secret(
    env_var: str, default: str | int | None = None
) -> str | int | None:
    """
    Get the value of an environment variable or read it from a file if it ends with _FILE.

    :param env_var: The variable name.
    :type env_var: str
    :param default: The default value of the variable.
    :type default: str | int | None
    :return: The variable value from the file or environment variable.
    :rtype: str | int | None
    """
    file_var = f"{env_var}_FILE"
    value = None
    if file_var in os.environ:
        # Read from file
        with open(os.environ[file_var], "r") as f:
            value = f.read().strip()
    else:
        # Read from environment variable
        value = os.getenv(env_var, default)
    return value


def load_config(app: Flask) -> None:
    """Load the config."""
    app.config.from_mapping(
        {
            "DB_HOST": _get_env_or_secret("POSTGRES_HOST"),
            "DB_NAME": _get_env_or_secret("POSTGRES_DB"),
            "DB_USER": _get_env_or_secret("POSTGRES_USER"),
            "DB_PASSWORD": _get_env_or_secret("POSTGRES_PASSWORD"),
            "DB_PORT": _get_env_or_secret("POSTGRES_PORT", "5432"),
            "FLASK_DEBUG": _get_env_or_secret("FLASK_DEBUG", "False"),
            "FLASK_HOST": _get_env_or_secret("FLASK_HOST", "127.0.0.1"),
            "SECRET_KEY": _get_env_or_secret("FLASK_SECRET_KEY"),
            "JWT_PRIVATE_KEY": _get_env_or_secret("JWT_PRIVATE_KEY"),
            "JWT_PUBLIC_KEY": _get_env_or_secret("JWT_PUBLIC_KEY"),
            "JWT_ALGORITHM": "ES512",
            "JWT_ACCESS_TOKEN_EXPIRES": timedelta(hours=1),
            "JWT_LEEWAY": timedelta(seconds=10),
            "BASE_URL": _get_env_or_secret("BASE_URL"),
            "PATH_PREFIX": _get_env_or_secret("PATH_PREFIX", ""),
        }
    )
