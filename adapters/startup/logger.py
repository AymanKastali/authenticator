from adapters.gateways.logging.logger_factory import create_console_json_logger
from adapters.interfaces.async_resource import AsyncResource
from application.ports.services.logger import LoggerPort


class LoggerResource(AsyncResource):
    """Async initializer for the app logger."""

    def __init__(self, name: str = "app_logger"):
        self._name: str = name
        self.logger: LoggerPort

    async def initialize(self) -> None:
        """Create and initialize the logger."""
        self.logger = create_console_json_logger(self._name)
        self.logger.info("[LoggerResource] Logger initialized")

    async def shutdown(self) -> None:
        """Log shutdown event."""
        if self.logger:
            self.logger.info("[LoggerResource] Logger shutdown")
