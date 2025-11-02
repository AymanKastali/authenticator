from adapters.config.jwt import JwtConfig
from adapters.controllers.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserController,
)
from adapters.controllers.auth.jwt.login import LoginJwtController
from adapters.controllers.auth.jwt.logout import LogoutJwtController
from adapters.controllers.auth.jwt.refresh_token import (
    RefreshJwtTokenController,
)
from adapters.controllers.auth.jwt.verify_token import VerifyJwtTokenController
from adapters.gateways.authentication.jwt_service import JwtService
from application.ports.services.jwt import JwtServicePort
from application.ports.services.logger import LoggerPort
from application.services.auth.authentication import AuthService
from application.services.auth.jwt.auth import JwtAuthService
from application.services.auth.jwt.facade import JwtAuthFacade
from application.use_cases.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserUseCase,
)
from delivery.db.in_memory.repositories import get_in_memory_user_repository
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
    """Container for JWT-based authentication (sync __init__)"""

    # def __init__(self, logger: LoggerPort, redis_client: Redis):
    # FIXME inject redis client
    def __init__(self, logger: LoggerPort):
        # Logger
        self.logger = logger

        # Redis client (already connected)
        # redis_manager = get_redis_connection_manager()
        # self.redis_client = redis_manager.get_client()

        # Infrastructure
        jwt_cfg = JwtConfig()
        self.jwt_service: JwtServicePort = JwtService(jwt_cfg)

        # Cache
        # self.get_jwt_blacklist_adapter = get_jwt_blacklist_adapter(
        #     self.redis_client
        # )

        # Repositories
        self.user_repo = get_in_memory_user_repository()

        # Services
        self.auth_service = AuthService(self.user_repo)
        self.jwt_auth_service = JwtAuthService(self.jwt_service)
        self.jwt_facade_service = JwtAuthFacade(
            auth_service=self.auth_service,
            jwt_auth_service=self.jwt_auth_service,
            # blacklist_cache=self.get_jwt_blacklist_adapter,
        )

        # Use cases
        self.get_authenticated_user_uc = GetAuthenticatedUserUseCase(
            user_repo=self.user_repo
        )

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
        self.authenticated_user_controller = GetAuthenticatedUserController(
            use_case=self.get_authenticated_user_uc
        )
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
        self.jwt_logout_handler = JwtLogoutHandler(
            controller=self.jwt_logout_controller, logger=self.logger
        )

        self.logger.info("[JwtAuthContainer] fully initialized")
