from redis.asyncio import ConnectionPool, Redis

from application.ports.services.logger import LoggerPort
from infrastructure.config.cache import RedisConfig


class AsyncRedisConnection:
    """
    Singleton-style manager for Redis connection.
    Handles connect/disconnect and exposes the Redis client.
    """

    _instance: "AsyncRedisConnection | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: RedisConfig, logger: LoggerPort):
        if not hasattr(self, "_initialized"):
            self._initialized: bool = False

        if self._initialized:
            return

        self._config = config
        self._logger = logger
        self._client: Redis | None = None
        self._pool: ConnectionPool | None = None
        self._initialized = True

    async def connect(self) -> Redis | None:
        if not self._config.is_enabled:
            self._logger.info("[Redis] Disabled via configuration")
            return None

        if self._client is None:
            self._pool = ConnectionPool.from_url(
                str(self._config.url),
                encoding="utf-8",
                decode_responses=True,
                max_connections=self._config.max_connections,
            )
            self._client = Redis(connection_pool=self._pool)
            if await self.ping():
                self._logger.info("[Redis] Connected successfully")
            else:
                self._logger.warning("[Redis] Ping failed")
        return self._client

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
            self._client = None
        if self._pool:
            await self._pool.disconnect()
            self._pool = None
        self._logger.info("[Redis] Disconnected")

    async def ping(self) -> bool:
        if self._client is None:
            return False
        try:
            return await self._client.ping()  # type: ignore
        except Exception:
            return False

    @property
    def client(self) -> Redis | None:
        """Return Redis client, or None if not connected / disabled."""
        return self._client
