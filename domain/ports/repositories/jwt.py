from abc import ABC, abstractmethod


class JwtBlacklistRepositoryPort(ABC):
    """Domain-level port for managing JWT blacklisting."""

    @abstractmethod
    async def add(self, jti: str, expires_at: int) -> None: ...

    @abstractmethod
    async def contains(self, jti: str) -> bool: ...
