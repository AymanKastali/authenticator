from adapters.gateways.logging.logger_factory import create_logger_adapter
from application.ports.services.logger import LoggerPort

from .app.policy import AppContainer
from .user import UserContainer

logger: LoggerPort = create_logger_adapter()


user_container = UserContainer(logger)
app_container = AppContainer()
