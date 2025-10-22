from application.services.auth_session import SessionAuthService
from domain.entities.user import User
from domain.value_objects.email import EmailAddress


class SessionLoginUseCase:
    def __init__(self, session_auth_service: SessionAuthService):
        self.session_auth_service = session_auth_service

    def execute(self, email: str, password: str) -> str | None:
        """
        Authenticate the user and create a session.
        Returns session ID if successful, else None.
        """
        user: User | None = self.session_auth_service.authenticate_local(
            EmailAddress(email), password
        )
        if not user:
            return None
        return self.session_auth_service.create_session(user)
