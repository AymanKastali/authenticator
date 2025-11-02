from typing import cast

from pydantic import Field, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    """Configuration for Redis connection."""

    url: RedisDsn = Field(default=cast(RedisDsn, "redis://localhost:6379/0"))
    max_connections: int = Field(default=10)
    db: int = Field(default=0)

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Validators
    @field_validator("max_connections", "db")
    @classmethod
    def non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("must be 0 or greater")
        return v
