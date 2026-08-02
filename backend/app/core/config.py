from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Knowledge Assistant API"
    app_version: str = "0.1.0"
    app_env: str = "development"

    database_url: str = ""
    database_echo: bool = False
    database_pool_size: int = 20
    database_max_overflow: int = 10
    database_pool_timeout: int = 30
    database_pool_recycle: int = 1800
    database_pool_pre_ping: bool = True

    api_prefix: str = "/api"
    api_version: str = "v1"

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    upload_directory: str = ""
    max_upload_size: int = 20 * 1024 * 1024

    allowed_content_types: str = ""
    @property
    def allowed_content_types_list(self) -> list[str]:
        return [
            item.strip()
            for item in self.allowed_content_types.split(",")
            if item.strip()
        ]

    allowed_extensions: str = ""
    @property
    def allowed_extensions_list(self) -> list[str]:
        return [
            item.strip()
            for item in self.allowed_extensions.split(",")
            if item.strip()
        ]

    supported_llm_providers: str = ""
    @property
    def supported_llm_providers_list(self) -> list[str]:
        return [
            item.strip()
            for item in self.supported_llm_providers.split(",")
            if item.strip()
        ]

    worker_enabled: bool = True
    worker_poll_interval: int = 5
    worker_batch_size: int = 10
    worker_interval_seconds: int = 10

    chunk_size: int = 1000
    chunk_overlap: int = 200

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()