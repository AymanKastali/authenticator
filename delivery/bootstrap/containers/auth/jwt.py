from adapters.config.jwt import JwtConfig
from adapters.controllers.auth.jwt.login import LoginJwtController
from adapters.controllers.auth.jwt.logout import LogoutJwtController
from adapters.controllers.auth.jwt.me import ReadMeController
from adapters.controllers.auth.jwt.refresh_token import (
    RefreshJwtTokenController,
)
from adapters.controllers.auth.jwt.verify_token import (
    VerifyJwtTokenController,
)
from adapters.gateways.authentication.jwt_service import JwtService
from application.ports.services.jwt import JwtServicePort
from application.ports.services.logger import LoggerPort
from application.services.auth.authentication import AuthService
from application.services.auth.jwt.auth import JwtAuthService
from application.services.auth.jwt.facade import JwtAuthFacade
from application.use_cases.auth.jwt.me import ReadMeUseCase
from delivery.db.in_memory.repositories import (
    get_in_memory_jwt_repository,
    get_in_memory_user_repository,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.get_me import ReadMeHandler
from delivery.web.fastapi.api.v1.handlers.auth.jwt.login import JwtLoginHandler
from delivery.web.fastapi.api.v1.handlers.auth.jwt.logout import (
    JwtLogoutHandler,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.refresh_token import (
    RefreshJwtTokenHandler,
)
from delivery.web.fastapi.api.v1.handlers.auth.jwt.verify_token import (
    VerifyJwtTokenHandler,
)


class JwtAuthContainer:
    """Container for jwt-based authentication"""

    def __init__(self, logger: LoggerPort):
        # Logger
        self.logger = logger

        # Infrastructure
        jwt_cfg = JwtConfig()
        self.jwt_service: JwtServicePort = JwtService(jwt_cfg)

        # Repositories
        self.user_repo = get_in_memory_user_repository()
        self.jwt_repo = get_in_memory_jwt_repository()

        # Services
        self.auth_service = AuthService(self.user_repo)
        self.jwt_auth_service = JwtAuthService(self.jwt_service)
        self.jwt_facade_service = JwtAuthFacade(
            auth_service=self.auth_service,
            jwt_auth_service=self.jwt_auth_service,
            jwt_repo=self.jwt_repo,
        )

        # Use cases
        self.get_user_use_case = ReadMeUseCase(user_repo=self.user_repo)
        self.read_me_uc = ReadMeUseCase(user_repo=self.user_repo)

        # Controllers
        self.jwt_login_controller = LoginJwtController(
            service=self.jwt_facade_service
        )
        self.jwt_refresh_token_controller = RefreshJwtTokenController(
            service=self.jwt_facade_service
        )
        self.verify_jwt_token_controller = VerifyJwtTokenController(
            service=self.jwt_facade_service
        )
        self.read_me_controller = ReadMeController(use_case=self.read_me_uc)
        self.jwt_logout_controller = LogoutJwtController(
            service=self.jwt_facade_service
        )

        # Handlers
        self.jwt_login_handler = JwtLoginHandler(
            controller=self.jwt_login_controller, logger=self.logger
        )
        self.jwt_refresh_token_handler = RefreshJwtTokenHandler(
            controller=self.jwt_refresh_token_controller, logger=self.logger
        )
        self.verify_jwt_token_handler = VerifyJwtTokenHandler(
            controller=self.verify_jwt_token_controller, logger=self.logger
        )
        self.read_me_handler = ReadMeHandler(
            controller=self.read_me_controller, logger=self.logger
        )
        self.jwt_logout_handler = JwtLogoutHandler(
            controller=self.jwt_logout_controller, logger=self.logger
        )
