from functools import lru_cache

from redis.asyncio import Redis

from adapters.config.cache import RedisSettings
from adapters.gateways.persistence.cache.redis.asynchronous.blacklist_adpater import (
    AsyncJwtBlacklistRedisAdapter,
)
from adapters.gateways.persistence.cache.redis.asynchronous.connection import (
    AsyncRedisConnectionManager,
)
from adapters.gateways.persistence.cache.redis.asynchronous.redis_adapter import (
    AsyncRedisAdapter,
)


@lru_cache()
def get_redis_connection_manager() -> AsyncRedisConnectionManager:
    """Return a singleton AsyncRedisConnectionManager instance."""
    settings = RedisSettings()
    return AsyncRedisConnectionManager(
        redis_url=str(settings.url),
        max_connections=settings.max_connections,
    )


async def get_redis_client() -> Redis:
    """Async Redis client dependency."""
    manager = get_redis_connection_manager()
    return await manager.connect()


@lru_cache()
def get_jwt_blacklist_adapter(
    redis_client: Redis,
) -> AsyncJwtBlacklistRedisAdapter:
    """Return a singleton JWT blacklist adapter."""
    return AsyncJwtBlacklistRedisAdapter(redis_client)


@lru_cache()
def get_cache_adapter_instance(redis_client: Redis) -> AsyncRedisAdapter:
    """Return a singleton general cache adapter."""
    return AsyncRedisAdapter(redis_client)
