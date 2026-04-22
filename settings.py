from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    TTLOCK_CLIENT_ID: str | None = None
    TTLOCK_CLIENT_SECRET: str | None = None
    TTLOCK_USERNAME: str | None = None
    TTLOCK_PASSWORD: str | None = None
    TTLOCK_API_URL: str = "https://api.ttlock.com"


settings = Settings()  # type: ignore
