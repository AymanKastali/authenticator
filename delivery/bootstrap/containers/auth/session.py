from adapters.controllers.auth_controllers.login_session_controller import (
    SessionLoginController,
)
from application.services.auth_session import SessionAuthService
from application.use_cases.auth_use_cases.session_login_uc import (
    SessionLoginUseCase,
)
from delivery.db.in_memory.repositories import (
    get_in_memory_session_repository,
    get_in_memory_user_repository,
)
from delivery.web.fastapi.api.v1.handlers.auth_handlers.login_session_handler import (
    SessionLoginHandler,
)


class SessionAuthContainer:
    """Container for session-based authentication (login/logout/refresh)"""

    def __init__(self):
        # Repositories
        self.user_repo = get_in_memory_user_repository()
        self.session_repo = get_in_memory_session_repository()

        # Services
        self.session_auth_service = SessionAuthService(
            user_repo=self.user_repo,
            session_repo=self.session_repo,
        )

        # Use Cases
        self.session_login_uc = SessionLoginUseCase(
            session_auth_service=self.session_auth_service
        )

        # Controllers
        self.session_login_controller = SessionLoginController(
            use_case=self.session_login_uc
        )

        # Handlers
        self.session_login_handler = SessionLoginHandler(
            controller=self.session_login_controller
        )
