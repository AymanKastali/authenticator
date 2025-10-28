from application.dto.user_dto import PersistenceUserDto
from application.services.auth_session import SessionAuthService


class SessionLoginUseCase:
    def __init__(self, session_auth_service: SessionAuthService):
        self.session_auth_service = session_auth_service

    def execute(self, email: str, password: str) -> str | None:
        """
        Authenticate the user and create a session.
        Returns session ID if successful, else None.
        """
        user: PersistenceUserDto | None = (
            self.session_auth_service.authenticate_user_local(email, password)
        )
        if not user:
            return None
        return self.session_auth_service.create_session(user)
