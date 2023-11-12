"""Settings management."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application, read from the environment."""

    database_host: str
    database_user: str
    database_password: str
    database_name: str
    database_port: int = 3306
    email_service_base_url: str
    email_service_endpoint: str = "/email"
    email_service_timeout_seconds: int = 5
    from_email: str = "app@example.com"
    code_expiration_seconds: int = 60


@lru_cache
def get_settings():
    """Dependency to retrieve settings.

    The settings are cached to avoid reading the environment multiple times.
    """
    return Settings()
