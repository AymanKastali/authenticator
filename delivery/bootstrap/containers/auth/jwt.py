from adapters.config.jwt_config import JwtConfig
from adapters.controllers.auth_controllers.jwt_login_controller import (
    JwtLoginController,
)
from adapters.controllers.auth_controllers.jwt_refresh_token_controller import (
    JwtRefreshTokenController,
)
from adapters.controllers.jwt.get_request_user_controller import (
    GetRequestUserController,
)
from adapters.gateways.authentication.jwt_service import JwtService
from application.ports.jwt_token_service_port import JwtTokenServicePort
from application.services.jwt_auth_service import JwtAuthService
from application.use_cases.user_use_cases.get_request_user_uc import (
    GetRequestUserUseCase,
)
from delivery.db.in_memory.repositories import get_in_memory_user_repository
from delivery.web.fastapi.api.v1.handlers.auth_handlers.jwt_login_handler import (
    JwtLoginHandler,
)
from delivery.web.fastapi.api.v1.handlers.auth_handlers.jwt_refresh_token_handler import (
    JwtRefreshTokenHandler,
)


class JwtAuthContainer:
    """Container for jwt-based authentication"""

    def __init__(self):
        # Infrastructure
        jwt_cfg = JwtConfig()
        self.jwt_service: JwtTokenServicePort = JwtService(jwt_cfg)

        # Repositories
        self.user_repo = get_in_memory_user_repository()

        # Services
        self.jwt_auth_service = JwtAuthService(
            user_repo=self.user_repo, jwt_service=self.jwt_service
        )

        # Use cases
        self.get_user_use_case = GetRequestUserUseCase(user_repo=self.user_repo)

        # Controllers
        self.get_user_controller = GetRequestUserController(
            use_case=self.get_user_use_case
        )
        self.jwt_login_controller = JwtLoginController(
            service=self.jwt_auth_service
        )
        self.jwt_refresh_token_controller = JwtRefreshTokenController(
            service=self.jwt_auth_service
        )

        # Handlers
        self.jwt_login_handler = JwtLoginHandler(
            controller=self.jwt_login_controller
        )
        self.jwt_refresh_token_handler = JwtRefreshTokenHandler(
            controller=self.jwt_refresh_token_controller
        )
