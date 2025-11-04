from functools import lru_cache

from redis.asyncio import Redis

from adapters.config.cache import RedisConfig
from adapters.gateways.persistence.cache.redis.asynchronous.connection import (
    AsyncRedisConnectionManager,
)


@lru_cache
def redis_config_dependency() -> RedisConfig:
    """Provide cached RedisConfig (singleton)."""
    return RedisConfig()


async def get_redis_connection_manager() -> AsyncRedisConnectionManager | None:
    """Return a singleton AsyncRedisConnectionManager instance."""
    config = redis_config_dependency()
    if not config.is_enabled:
        return None
    return AsyncRedisConnectionManager(
        redis_url=str(config.url),
        max_connections=config.max_connections,
    )


async def get_redis_client() -> Redis | None:
    """Async Redis client dependency."""
    manager = await get_redis_connection_manager()
    if manager is None:
        return None
    connected: bool = await manager.ping()
    if connected is True:
        return await manager.get_client()
    return await manager.connect()
