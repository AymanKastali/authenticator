from functools import lru_cache

from infrastructure.config.cache import RedisConfig
from infrastructure.config.jwt import JwtConfig


@lru_cache
def jwt_config() -> JwtConfig:
    """Provide cached JwtDomainConfig (singleton)."""
    return JwtConfig()


@lru_cache
def get_redis_config() -> RedisConfig:
    """Provide cached RedisConfig (singleton)."""
    return RedisConfig()
