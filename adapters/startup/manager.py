from adapters.interfaces.async_resource import AsyncResource
from adapters.startup.logger import LoggerResource
from adapters.startup.redis import RedisResource
from application.ports.services.logger import LoggerPort


class ResourceManager(AsyncResource):
    """Manages all async resources and ensures correct init/shutdown order."""

    def __init__(self):
        self.logger_resource: LoggerResource = LoggerResource()
        self.logger: LoggerPort
        self.resources: list[AsyncResource] = []

    async def initialize(self) -> None:
        await self.logger_resource.initialize()
        self.logger = self.logger_resource.logger

        self.resources = [
            RedisResource(logger=self.logger),
            # Add other resources here
        ]

        self.logger.info("[ResourceManager] Initializing all resources...")
        for resource in self.resources:
            await resource.initialize()
        self.logger.info("[ResourceManager] All resources initialized")

    async def shutdown(self) -> None:
        self.logger.info("[ResourceManager] Shutting down all resources...")
        for resource in reversed(self.resources):
            await resource.shutdown()
        await self.logger_resource.shutdown()
        self.logger.info("[ResourceManager] All resources shut down")
