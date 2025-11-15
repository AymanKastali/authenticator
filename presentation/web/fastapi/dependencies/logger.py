from application.ports.services.logger import LoggerPort
from infrastructure.gateways.logging.factory import (
    create_console_json_logger,
)


def get_console_json_logger() -> LoggerPort:
    """Provide application logger."""
    return create_console_json_logger()
