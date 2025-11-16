from abc import ABC, abstractmethod


class JwtRedisRepositoryPort(ABC):
    """Abstract port for managing JWT blacklist."""

    @abstractmethod
    async def blacklist_jwt(self, jti: str, expire_at: float) -> None: ...

    @abstractmethod
    async def is_jwt_blacklisted(self, jti: str) -> bool: ...
