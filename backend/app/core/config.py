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
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    QR_HMAC_SECRET_KEY: str = ""
    PUBLIC_QR_BASE_URL: str = ""


def get_settings() -> Settings:
    return Settings()
