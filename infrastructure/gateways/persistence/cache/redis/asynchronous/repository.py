from datetime import datetime, timezone

from redis.asyncio import Redis, RedisError

from application.ports.repositories.jwt import JwtRedisRepositoryPort


class JwtRedisRepository(JwtRedisRepositoryPort):
    """Adapter for JWT blacklisting using a Redis sorted set."""

    BLACKLIST_SET_KEY = "blacklisted_jtis"

    def __init__(self, redis_client: Redis | None):
        self._client = redis_client

    async def blacklist_jwt(self, jti: str, expire_at: float) -> None:
        """Add a JWT to the blacklist with expiration timestamp."""
        if not self._client:
            return
        try:
            await self._client.zadd(
                self.BLACKLIST_SET_KEY,
                {jti: expire_at},
            )
        except RedisError:
            pass

    async def is_jwt_blacklisted(self, jti: str) -> bool:
        """Check if a JWT is blacklisted, pruning expired tokens."""
        if not self._client:
            return False
        try:
            now_ts = int(datetime.now(timezone.utc).timestamp())
            await self._client.zremrangebyscore(
                self.BLACKLIST_SET_KEY, 0, now_ts
            )
            return (
                await self._client.zscore(self.BLACKLIST_SET_KEY, jti)
            ) is not None
        except RedisError:
            return False
