"""Settings management."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application, read from the environment."""

    database_host: str = "localhost"
    database_user: str = "mysql"
    database_password: str = "mysql"
    database_name: str = "mysql"
    database_port: int = 3306
    smtp_host: str = ""
    smtp_port: int = 0


@lru_cache
def get_settings():
    """Dependency to retrieve settings.

    The settings are cached to avoid reading the environment multiple times.
    """
    return Settings()
