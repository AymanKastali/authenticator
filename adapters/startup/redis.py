from adapters.config.cache import RedisConfig
from adapters.gateways.persistence.cache.redis.asynchronous.connection import (
    AsyncRedisConnectionManager,
)
from adapters.interfaces.async_resource import AsyncResource
from application.ports.services.logger import LoggerPort


class RedisResource(AsyncResource):
    """Async initializer for Redis."""

    def __init__(self, logger: LoggerPort):
        self.logger: LoggerPort = logger
        self.config: RedisConfig = RedisConfig()
        self.redis: AsyncRedisConnectionManager | None = None

    async def initialize(self) -> None:
        """Initialize Redis connection."""
        self.logger.info("[RedisResource] Initializing Redis...")

        if self.config.is_enabled:
            self.logger.info("[Redis] Configuration detected — initializing...")
            redis = AsyncRedisConnectionManager(
                redis_url=str(self.config.url),
                max_connections=self.config.max_connections,
            )
            await redis.connect()
            if await redis.ping():
                self.logger.info("[Redis] Connected successfully")
            else:
                self.logger.warning("[Redis] Unable to connect")
            self.redis = redis
        else:
            self.logger.info("[Redis] Skipped (no URL configured)")

    async def shutdown(self) -> None:
        """Shutdown Redis connection."""
        self.logger.info("[RedisResource] Shutting down Redis...")
        if self.redis is not None:
            await self.redis.disconnect()
            self.logger.info("[Redis] Disconnected")
