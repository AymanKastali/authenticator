from adapters.controllers.auth_controllers.register_user_controller import (
    RegisterUserController,
)
from adapters.validators.password_validators.complexity_password_validator import (
    ComplexityPasswordValidator,
)
from adapters.validators.password_validators.length_password_validator import (
    LengthPasswordValidator,
)
from application.services.password_service import PasswordService
from application.use_cases.auth_use_cases.register_user_uc import (
    RegisterUserUseCase,
)
from delivery.db.in_memory.repositories import get_in_memory_user_repository
from delivery.web.fastapi.api.v1.handlers.auth_handlers.register_user_handler import (
    RegisterUserHandler,
)


class RegistrationContainer:
    """Container for user registration and password validation"""

    def __init__(self):
        # Repository
        self.user_repo = get_in_memory_user_repository()

        # Services
        validators = [
            LengthPasswordValidator(min_length=8, max_length=128),
            ComplexityPasswordValidator(),
        ]
        self.password_service = PasswordService(validators=validators)

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
