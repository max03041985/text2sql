from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Database ---
    DATABASE_URL: str = "postgresql+asyncpg://postgres:Samplepg@localhost:5432/accrualdb"
    DB_TYPE: Literal["postgres", "greenplum"] = "postgres"

    # --- LLM ---
    OLLAMA_URL: str = "http://localhost:11434/api/chat"
    LLM_MODEL: str = "qwen3.5:4b"
    LLM_TEMPERATURE: float = 0.1
    LLM_TIMEOUT: int = 600

    # --- Query Governance ---
    STATEMENT_TIMEOUT: str = "600s"
    WORK_MEM: str = "256MB"
    MAX_STREAM_ROWS: int = 2_000_000
    DISTRIBUTION_KEY: str = "unique_customer_id"

    # --- Greenplum-specific ---
    GP_STATEMENT_MEM: str = "1GB"
    GP_MAX_CURSOR_MEMORY: str = "512MB"

    # --- API/UI ---
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    UI_HOST: str = "0.0.0.0"
    UI_PORT: int = 8501
    CORS_ORIGINS: str = "*"
    API_BASE_URL: str = "http://localhost:8000"
    API_REQUEST_TIMEOUT: int = 1230

    # --- Logging ---
    LOG_LEVEL: str = "INFO"
    SQLALCHEMY_ECHO: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()
