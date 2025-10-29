from adapters.controllers.auth.session.login import (
    SessionLoginController,
)
from application.services.auth.session import SessionAuthService
from delivery.db.in_memory.repositories import (
    get_in_memory_session_repository,
    get_in_memory_user_repository,
)
from delivery.web.fastapi.api.v1.handlers.auth.session.login import (
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

        # Controllers
        self.session_login_controller = SessionLoginController(
            service=self.session_auth_service
        )

        # Handlers
        self.session_login_handler = SessionLoginHandler(
            controller=self.session_login_controller
        )
