from adapters.controllers.auth.registration.register import (
    RegisterUserController,
)
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
from domain.policies.password.complexity import PasswordComplexityPolicy
from domain.policies.password.length import PasswordLengthPolicy


class RegistrationContainer:
    """Container for user registration and password validation"""

    def __init__(self):
        # Repository
        self.user_repo = get_in_memory_user_repository()

        # Services
        policies = [
            PasswordLengthPolicy(min_length=8, max_length=128),
            PasswordComplexityPolicy(),
        ]
        self.password_service = PasswordService(policies)

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
            controller=self.register_user_controller
        )
