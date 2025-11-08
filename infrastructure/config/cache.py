from pydantic import Field, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisConfig(BaseSettings):
    """Configuration for Redis connection."""

    url: RedisDsn | None = Field(
        default=None,
        description="Redis connection URL (optional — if not set, Redis will be disabled)",
    )
    max_connections: int = Field(default=10)

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def is_enabled(self) -> bool:
        """Whether Redis is configured and should be used."""
        return self.url is not None

    @field_validator("max_connections", "db")
    @classmethod
    def non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("must be 0 or greater")
        return v
