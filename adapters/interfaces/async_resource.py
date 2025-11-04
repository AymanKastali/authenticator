from abc import ABC, abstractmethod


class AsyncResource(ABC):
    """Base interface for any resource that needs async init/shutdown."""

    @abstractmethod
    async def initialize(self) -> None: ...

    @abstractmethod
    async def shutdown(self) -> None: ...
