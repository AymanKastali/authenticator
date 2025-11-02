from datetime import datetime, timezone

from redis.asyncio import Redis

from application.ports.cache.redis.jwt_blacklist import (
    AsyncJwtBlacklistRedisPort,
)


class AsyncJwtBlacklistRedisAdapter(AsyncJwtBlacklistRedisPort):
    """Adapter for JWT blacklisting using a Redis sorted set."""

    BLACKLIST_SET_KEY = "blacklisted_jtis"

    def __init__(self, redis_client: Redis):
        self._client = redis_client

    async def blacklist_jwt(self, jti: str, expire_at: int) -> None:
        """Add a JWT to the blacklist with expiration timestamp."""
        await self._client.zadd(self.BLACKLIST_SET_KEY, {jti: expire_at})

    async def is_jwt_blacklisted(self, jti: str) -> bool:
        """Check if a JWT is blacklisted, pruning expired tokens."""
        now_ts = int(datetime.now(timezone.utc).timestamp())
        await self._client.zremrangebyscore(self.BLACKLIST_SET_KEY, 0, now_ts)
        return (
            await self._client.zscore(self.BLACKLIST_SET_KEY, jti) is not None
        )
