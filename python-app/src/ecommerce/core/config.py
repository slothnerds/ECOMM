"""Typed application settings (the Python counterpart of AppProperties.java).

Values come from, in order of priority:
1. real environment variables
2. python-app/.env.<profile>  (database settings; profile from APP_PROFILE: local | docker)
3. python-app/.env            (settings shared by every profile)
4. the defaults below

Pydantic validates them when Settings() is created, so a bad value stops startup.
"""

import os
from datetime import timedelta
from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

Profile = Literal["local", "docker"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Relative to the working directory, so start the app from python-app/.
        # get_settings() adds the profile file on top of this.
        env_file=".env",
        env_file_encoding="utf-8",
        # Ignore .env entries this class doesn't declare instead of failing
        extra="ignore",
    )

    app_name: str = "E-Commerce POC"
    # Which database to use (like Spring's local/docker profiles)
    profile: Profile = Field(default="local", alias="APP_PROFILE")
    # Field names map to env vars case-insensitively; alias picks a different name
    environment: Literal["dev", "test", "prod"] = Field(default="dev", alias="APP_ENV")
    # SecretStr prints as '**********' in logs, repr() and str()
    jwt_secret: SecretStr = Field(min_length=32)
    # Parses ISO-8601 durations such as PT15M
    hold_duration: timedelta = timedelta(minutes=15)
    port: int = 8000

    # Database (defaults = the "local" profile: PostgreSQL installed on this machine)
    db_host: str = "localhost"
    db_port: int = 5433
    db_name: str = "ecomm_db"
    db_user: str = "postgres"
    db_password: SecretStr = SecretStr("password")
    # Seconds to wait for a new database connection before failing
    db_connect_timeout_s: int = Field(default=3, ge=1)

    @property
    def database_url(self) -> str:
        """SQLAlchemy URL (dialect+driver://user:password@host:port/db); contains the password."""
        password = self.db_password.get_secret_value()
        return (
            f"postgresql+psycopg://{self.db_user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def database_display(self) -> str:
        """The database location without the password, safe to log."""
        return f"{self.db_host}:{self.db_port}/{self.db_name} as user {self.db_user}"


@lru_cache
def get_settings() -> Settings:
    """Create Settings once and reuse it (use with FastAPI's Depends(get_settings))."""
    profile = os.environ.get("APP_PROFILE", "local")
    # Later files win: the profile file overrides the shared .env
    return Settings(_env_file=(".env", f".env.{profile}"))
