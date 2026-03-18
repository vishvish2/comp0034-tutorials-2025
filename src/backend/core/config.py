import secrets
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    db_name: str
    db_driver: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        return f"{self.db_driver}{BASE_DIR}/src/data/{self.db_name}"


def get_settings():
    settings = Settings()
    return settings