from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Knowledge Assistant API"
    app_version: str = "0.1.0"
    app_env: str = "development"

    api_prefix: str = "/api"
    api_version: str = "v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()