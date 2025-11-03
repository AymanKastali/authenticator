from adapters.gateways.logging.logger_factory import create_console_json_logger
from application.ports.services.logger import LoggerPort


def get_console_json_logger() -> LoggerPort:
    """Provide application logger."""
    return create_console_json_logger()
