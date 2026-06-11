"""
The Settings class.
module: src/config/settings.py
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Manage environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        secrets_dir="/run/secrets",
        env_ignore_empty=True,
    )

    db_host: str = Field(validation_alias="POSTGRES_HOST")
    db_port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    db_name: str = Field(validation_alias="POSTGRES_DB")
    db_user: str = Field(validation_alias="POSTGRES_USER")
    db_password: str = Field(validation_alias="POSTGRES_PASSWORD")
    base_url: str = Field(validation_alias="BASE_URL")
