from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.

    This class centralizes configuration management using
    pydantic-settings and supports .env file loading.
    """

    # Application
    app_name: str = "SmartRecruitz"
    environment: str = "local"
    debug: bool = False

    # Database
    database_url: str

    # Redis / Celery
    redis_url: str

    # AI Keys (future usage)
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.

    Returns:
        Settings: Loaded configuration object.
    """
    return Settings()


settings = get_settings()
