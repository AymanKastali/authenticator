from application.ports.services.logger import LoggerPort
from infrastructure.config.cache import RedisConfig
from infrastructure.gateways.persistence.cache.redis.asynchronous.connection import (
    AsyncRedisConnectionManager,
)


async def init_redis(
    redis_config: RedisConfig, logger: LoggerPort
) -> AsyncRedisConnectionManager | None:
    """Initialize Redis if URL is provided and attach to app.state."""
    if redis_config.is_enabled is False:
        return None

    url: str = str(redis_config.url)
    redis_manager = AsyncRedisConnectionManager(
        url=url,
        max_connections=redis_config.max_connections,
    )
    _ = await redis_manager.connect()
    connected: bool = await redis_manager.ping()
    if connected is True:
        logger.info("[Redis] Connected successfully")
    else:
        logger.warning("[Redis] Ping failed")
    return redis_manager
