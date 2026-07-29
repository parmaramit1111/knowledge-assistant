from pydantic import Field, field_validator
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Knowledge Assistant API"
    app_version: str = "0.1.0"
    app_env: str = "development"

    api_prefix: str = "/api"
    api_version: str = "v1"

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    upload_directory: str = ""
    max_upload_size: int = 20 * 1024 * 1024
    allowed_content_types: list[str] = Field(default_factory=list)

    @field_validator("allowed_content_types", mode="before")
    @classmethod
    def parse_allowed_content_types(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()