from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    app_name: str = "Knowledge Assistant API"
    app_version: str = "0.1.0"
    app_env: str = "development"

    database_host: str = "127.0.0.1"
    database_port: int = 5433
    database_name: str = "knowledge_assistant"
    database_user: str = "postgres"
    database_password: str = ""

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.database_user,
            password=self.database_password,
            host=self.database_host,
            port=self.database_port,
            database=self.database_name,
        )

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

    embedding_provider: str = "sentence_transformers"
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()