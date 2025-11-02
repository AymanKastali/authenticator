from adapters.gateways.logging.logger_factory import create_logger_adapter
from application.dto.policies.password import PasswordPolicyConfigDto
from application.ports.services.logger import LoggerPort

from .jwt import JwtAuthContainer
from .registration import RegistrationContainer
from .session import SessionAuthContainer

logger: LoggerPort = create_logger_adapter()

password_policy_dto = PasswordPolicyConfigDto(
    min_length=8,
    max_length=128,
    require_upper=True,
    require_lower=True,
    require_digit=True,
    require_special=True,
)
# FIXME
jwt_auth_container = JwtAuthContainer(logger)
registration_container = RegistrationContainer(logger, password_policy_dto)
session_auth_container = SessionAuthContainer()
