"""
The Settings class.
module: src/config/settings.py
"""

from pydantic import Field, AliasChoices
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
    db_name: str = Field(validation_alias=AliasChoices("POSTGRES_DB", "db_name"))
    db_user: str = Field(validation_alias=AliasChoices("POSTGRES_USER", "db_user"))
    db_password: str = Field(
        validation_alias=AliasChoices("POSTGRES_PASSWORD", "db_password")
    )
    base_url: str = Field(validation_alias="BASE_URL")
    root_path: str = Field(default="", validation_alias="ROOT_PATH")
    public_key: str = Field(
        validation_alias=AliasChoices("JWT_PUBLIC_KEY", "jwt_public_key")
    )
