"""
The Settings class.
module: src/config/settings.py
"""

from pydantic_settings import BaseSettings
from .load_env import get_env_or_secret


class Settings(BaseSettings):
    """
    Manage environment variables.
    """

    db_host: str = str(get_env_or_secret("POSTGRES_HOST"))
    db_port: int = int(get_env_or_secret("POSTGRES_PORT", 5432))
    db_name: str = str(get_env_or_secret("POSTGRES_DB"))
    db_user: str = str(get_env_or_secret("POSTGRES_USER"))
    db_password: str = str(get_env_or_secret("POSTGRES_PASSWORD"))
