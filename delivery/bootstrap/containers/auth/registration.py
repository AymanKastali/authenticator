from adapters.controllers.auth.registration.register import (
    RegisterUserController,
)
from application.dto.policies.password import PasswordPolicyConfigDto
from application.ports.services.logger import LoggerPort
from application.services.auth.registration.password_service import (
    PasswordService,
)
from application.use_cases.auth.registration.register import (
    RegisterUserUseCase,
)
from delivery.db.in_memory.repositories import get_in_memory_user_repository
from delivery.web.fastapi.api.v1.handlers.auth.registration.register import (
    RegisterUserHandler,
)


class RegistrationContainer:
    """Container for user registration and password validation"""

    def __init__(
        self, logger: LoggerPort, password_policy: PasswordPolicyConfigDto
    ):
        # Repository
        self.user_repo = get_in_memory_user_repository()

        # Services
        self.password_service = PasswordService(policy_config=password_policy)

        # Use Cases
        self.register_user_uc = RegisterUserUseCase(
            user_repo=self.user_repo,
            password_service=self.password_service,
        )

        # Controllers
        self.register_user_controller = RegisterUserController(
            use_case=self.register_user_uc
        )

        # Handlers
        self.register_user_handler = RegisterUserHandler(
            controller=self.register_user_controller, logger=logger
        )
