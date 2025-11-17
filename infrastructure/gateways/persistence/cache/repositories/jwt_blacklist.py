from redis.asyncio import Redis

from domain.ports.repositories.jwt import JwtBlacklistRepositoryPort


class RedisJwtBlacklistRepository(JwtBlacklistRepositoryPort):
    """Redis-backed JWT blacklist repository (optional Redis)."""

    def __init__(self, redis_client: Redis | None):
        self._redis = redis_client

    async def add(self, jti: str, expires_at: int) -> None:
        if self._redis is None:
            return
        await self._redis.set(name=jti, value=1, ex=expires_at)

    async def contains(self, jti: str) -> bool:
        if self._redis is None:
            return False
        exists = await self._redis.exists(jti)
        return bool(exists)
