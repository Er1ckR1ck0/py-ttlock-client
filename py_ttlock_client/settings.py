import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = os.path.join(BASE_DIR, ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore")

    TTLOCK_CLIENT_ID: Optional[str] = None
    TTLOCK_CLIENT_SECRET: Optional[str] = None
    TTLOCK_USERNAME: Optional[str] = None
    TTLOCK_PASSWORD: Optional[str] = None


settings = Settings()  # type: ignore
