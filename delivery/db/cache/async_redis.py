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


async def get_redis_connection_manager() -> AsyncRedisConnectionManager:
    """Return a singleton AsyncRedisConnectionManager instance."""
    config = redis_config_dependency()
    return AsyncRedisConnectionManager(
        redis_url=str(config.url),
        max_connections=config.max_connections,
    )


async def get_redis_client() -> Redis:
    """Async Redis client dependency."""
    manager = await get_redis_connection_manager()
    connected: bool = await manager.ping()
    if connected is True:
        return await manager.get_client()
    return await manager.connect()
