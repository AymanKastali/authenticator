from adapters.gateways.logging.logger_factory import create_logger_adapter
from application.ports.services.logger import LoggerPort

from .jwt import JwtAuthContainer
from .registration import RegistrationContainer
from .session import SessionAuthContainer

logger: LoggerPort = create_logger_adapter()

jwt_auth_container = JwtAuthContainer(logger)
registration_container = RegistrationContainer(logger)
session_auth_container = SessionAuthContainer()
