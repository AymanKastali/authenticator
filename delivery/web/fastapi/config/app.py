from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Application configuration for the FastAPI delivery layer."""

    # === Basic App Info ===
    name: str = Field(default="authorizer", description="Service name")
    version: str = Field(default="1.0.0", description="Application version")
    environment: str = Field(
        default="development", description="Environment name"
    )
    debug: bool = Field(default=True, description="Enable debug mode")

    # === Server Settings ===
    host: str = Field(default="0.0.0.0", description="Host address")
    port: int = Field(default=8000, description="Port number")

    # === Other ===
    log_level: str = Field(default="INFO", description="Logging level")

    # === Model Configuration ===
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # === Validators ===
    @field_validator("name", "version", "environment", "host", "log_level")
    @classmethod
    def non_empty_string(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must be a non-empty string")
        return v

    @field_validator("port")
    @classmethod
    def valid_port(cls, v: int) -> int:
        if not (1 <= v <= 65535):
            raise ValueError("port must be between 1 and 65535")
        return v
