from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parents[3] / ".env"),
        env_file_encoding="utf-8",
    )

    DATABASE_URL: str
    BOOTSTRAP_ADMIN_PASSWORD: str | None = None
    BOOTSTRAP_ADMIN_USERNAME: str = "admin"
    BOOTSTRAP_ADMIN_FULL_NAME: str = "Administrator"
    BOOTSTRAP_ADMIN_ROLE_NAME: str = "Admin"


def get_settings() -> Settings:
    return Settings()
