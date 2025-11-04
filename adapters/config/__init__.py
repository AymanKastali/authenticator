from functools import lru_cache

from adapters.config.cache import RedisConfig


@lru_cache
def redis_config_dependency() -> RedisConfig:
    """Provide cached RedisConfig (singleton)."""
    return RedisConfig()
