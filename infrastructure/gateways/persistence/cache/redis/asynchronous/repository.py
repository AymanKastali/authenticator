from datetime import datetime, timezone

from redis.asyncio import Redis, RedisError

from domain.ports.repositories.jwt import JwtRedisRepositoryPort
from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.uuid_id import UUIDVo


class JwtRedisRepository(JwtRedisRepositoryPort):
    """Adapter for JWT blacklisting using a Redis sorted set."""

    BLACKLIST_SET_KEY = "blacklisted_jtis"

    def __init__(self, redis_client: Redis | None):
        self._client = redis_client

    async def blacklist_jwt(self, jti: UUIDVo, expire_at: DateTimeVo) -> None:
        """Add a JWT to the blacklist with expiration timestamp."""
        if not self._client:
            return
        try:
            await self._client.zadd(
                self.BLACKLIST_SET_KEY,
                {jti.to_string(): expire_at.to_timestamp()},
            )
        except RedisError:
            pass

    async def is_jwt_blacklisted(self, jti: UUIDVo) -> bool:
        """Check if a JWT is blacklisted, pruning expired tokens."""
        if not self._client:
            return False
        try:
            now_ts = int(datetime.now(timezone.utc).timestamp())
            await self._client.zremrangebyscore(
                self.BLACKLIST_SET_KEY, 0, now_ts
            )
            return (
                await self._client.zscore(
                    self.BLACKLIST_SET_KEY, jti.to_string()
                )
            ) is not None
        except RedisError:
            return False
