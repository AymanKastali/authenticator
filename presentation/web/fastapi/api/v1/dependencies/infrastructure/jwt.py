from functools import lru_cache

from fastapi import Depends, Request
from redis.asyncio import Redis

from domain.ports.repositories.jwt import JwtRedisRepositoryPort
from domain.ports.services.jwt import JwtServicePort
from infrastructure.config import jwt_config
from infrastructure.config.jwt import JwtConfig
from infrastructure.gateways.auth.jwt import JwtService
from infrastructure.gateways.persistence.cache.redis.asynchronous.repository import (
    JwtRedisRepository,
)


@lru_cache
def jwt_config_dependency() -> JwtConfig:
    """Provide cached JwtConfig (singleton)."""
    return jwt_config()


def jwt_service_dependency(
    config: JwtConfig = Depends(jwt_config_dependency),
) -> JwtServicePort:
    """Provide JwtService implementation."""
    return JwtService(config)


async def jwt_redis_dependency(request: Request) -> JwtRedisRepositoryPort:
    redis_conn: Redis | None = getattr(request.app.state, "redis", None)
    return JwtRedisRepository(redis_conn)
