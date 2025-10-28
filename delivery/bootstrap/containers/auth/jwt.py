from adapters.config.jwt_config import JwtConfig
from adapters.controllers.auth.jwt.get_request_user import (
    GetRequestUserController,
)
from adapters.controllers.auth.jwt.login import LoginJwtController
from adapters.controllers.auth.jwt.refresh_token import (
    RefreshJwtTokenController,
)
from adapters.controllers.auth.jwt.verify_token import (
    VerifyJwtTokenController,
)
from adapters.gateways.authentication.jwt_service import JwtService
from application.ports.jwt_token_service_port import JwtTokenServicePort
from application.services.jwt_auth_service import JwtAuthService
from application.use_cases.user.get_request_user import (
    GetRequestUserUseCase,
)
from delivery.db.in_memory.repositories import get_in_memory_user_repository
from delivery.web.fastapi.api.v1.handlers.auth.jwt.login import JwtLoginHandler
from delivery.web.fastapi.api.v1.handlers.auth.jwt.refresh_token import (
    RefreshJwtTokenHandler,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.verify_token import (
    VerifyJwtTokenHandler,
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
        self.jwt_login_controller = LoginJwtController(
            service=self.jwt_auth_service
        )
        self.jwt_refresh_token_controller = RefreshJwtTokenController(
            service=self.jwt_auth_service
        )
        self.verify_jwt_token_controller = VerifyJwtTokenController(
            service=self.jwt_auth_service
        )

        # Handlers
        self.jwt_login_handler = JwtLoginHandler(
            controller=self.jwt_login_controller
        )
        self.jwt_refresh_token_handler = RefreshJwtTokenHandler(
            controller=self.jwt_refresh_token_controller
        )
        self.verify_jwt_token_handler = VerifyJwtTokenHandler(
            controller=self.verify_jwt_token_controller
        )
