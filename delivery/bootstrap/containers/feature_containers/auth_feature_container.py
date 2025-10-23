from adapters.controllers.auth_controllers.login_jwt_controller import (
    JwtLoginController,
)
from adapters.controllers.auth_controllers.login_session_controller import (
    SessionLoginController,
)
from adapters.controllers.auth_controllers.register_user_controller import (
    RegisterUserController,
)
from application.ports.jwt_token_service import JwtTokenServicePort
from application.services.auth_session import SessionAuthService
from application.services.authentication import AuthenticationService
from application.services.jwt_auth_service import JwtAuthService
from application.use_cases.auth_use_cases.jwt_login_uc import JwtLoginUseCase
from application.use_cases.auth_use_cases.register_user_uc import (
    RegisterUserUseCase,
)
from application.use_cases.auth_use_cases.session_login_uc import (
    SessionLoginUseCase,
)
from delivery.bootstrap.domain_config_factory import DomainConfigFactory
from delivery.db.in_memory.repositories import (
    get_in_memory_session_repository,
    get_in_memory_user_repository,
)
from delivery.web.fastapi.api.v1.handlers.auth_handlers.login_jwt_handler import (
    JwtLoginHandler,
)
from delivery.web.fastapi.api.v1.handlers.auth_handlers.login_session_handler import (
    SessionLoginHandler,
)
from delivery.web.fastapi.api.v1.handlers.auth_handlers.register_user_handler import (
    RegisterUserHandler,
)


class AuthFeatureContainer:
    def __init__(self, jwt_service: JwtTokenServicePort):
        # Infrastructure
        self.jwt_service = jwt_service

        # Repositories
        self.user_repo = get_in_memory_user_repository()
        self.session_repo = get_in_memory_session_repository()

        # Services
        self.jwt_auth_service = JwtAuthService(
            user_repo=self.user_repo, jwt_service=self.jwt_service
        )
        self.session_auth_service = SessionAuthService(
            user_repo=self.user_repo,
            session_repo=self.session_repo,
        )
        self.auth_service = AuthenticationService(user_repo=self.user_repo)

        # Use Cases
        self.jwt_login_uc = JwtLoginUseCase(
            jwt_auth_service=self.jwt_auth_service
        )
        self.session_login_uc = SessionLoginUseCase(
            session_auth_service=self.session_auth_service
        )
        self.register_user_uc = RegisterUserUseCase(
            user_repo=self.user_repo,
            password_cfg=DomainConfigFactory.load_password_config(),
        )

        # Controllers
        self.jwt_login_controller = JwtLoginController(
            use_case=self.jwt_login_uc
        )
        self.session_login_controller = SessionLoginController(
            use_case=self.session_login_uc
        )
        self.register_user_controller = RegisterUserController(
            use_case=self.register_user_uc
        )

        # Handlers
        self.jwt_login_handler = JwtLoginHandler(
            controller=self.jwt_login_controller
        )
        self.session_login_handler = SessionLoginHandler(
            controller=self.session_login_controller
        )
        self.register_user_handler = RegisterUserHandler(
            controller=self.register_user_controller
        )
