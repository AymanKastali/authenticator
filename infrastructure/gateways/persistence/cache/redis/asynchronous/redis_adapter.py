from typing import Any

from redis.asyncio import Redis

from application.ports.cache.redis.async_cache import AsyncRedisPort


class AsyncRedisAdapter(AsyncRedisPort):
    """General-purpose async Redis cache adapter."""

    def __init__(self, redis_client: Redis):
        self._client = redis_client

    async def get(self, key: str) -> Any | None:
        return await self._client.get(key)

    async def set(
        self, key: str, value: Any, expire: int | None = None
    ) -> None:
        await self._client.set(key, value, ex=expire)

    async def delete(self, key: str) -> None:
        await self._client.delete(key)

    async def clear(self) -> None:
        await self._client.flushdb()
