from abc import ABC, abstractmethod


class AsyncJwtBlacklistRedisPort(ABC):
    """Abstract port for managing JWT blacklist."""

    @abstractmethod
    async def blacklist_jwt(self, jti: str, expire_at: int) -> None: ...

    @abstractmethod
    async def is_jwt_blacklisted(self, jti: str) -> bool: ...
