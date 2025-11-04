from redis.asyncio import ConnectionPool, Redis


class AsyncRedisConnectionManager:
    """Singleton manager for Redis connection pool."""

    _instance: "AsyncRedisConnectionManager | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, url: str, max_connections: int = 10):
        if not hasattr(self, "_initialized"):
            self._initialized = False

        if self._initialized:
            return  # already initialized

        self._redis_url = url
        self._max_connections = max_connections
        self._client: Redis | None = None
        self._pool: ConnectionPool | None = None
        self._initialized = True

    async def connect(self) -> Redis:
        if self._client is None:
            self._pool = ConnectionPool.from_url(
                self._redis_url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=self._max_connections,
            )
            self._client = Redis(connection_pool=self._pool)
        return self._client

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
            self._client = None
        if self._pool:
            await self._pool.disconnect()
            self._pool = None

    def get_client(self) -> Redis:
        if self._client is None:
            raise RuntimeError(
                "Redis client not connected. Call `await connect()` first."
            )
        return self._client

    async def ping(self) -> bool:
        """Test if Redis connection is alive."""
        client = self.get_client()
        try:
            return await client.ping()  # type: ignore
        except Exception:
            return False

    # Async context manager
    async def __aenter__(self) -> "AsyncRedisConnectionManager":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()
