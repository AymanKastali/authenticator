from abc import ABC, abstractmethod
from typing import Any


class AsyncRedisPort(ABC):
    """Abstract port for async key-value cache."""

    @abstractmethod
    async def get(self, key: str) -> Any | None: ...

    @abstractmethod
    async def set(
        self, key: str, value: Any, expire: int | None = None
    ) -> None: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...

    @abstractmethod
    async def clear(self) -> None: ...
