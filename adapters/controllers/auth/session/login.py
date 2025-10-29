from fastapi import HTTPException

from adapters.dto.responses.auth.session.session import SessionOutDto
from application.services.auth.session import SessionAuthService


class SessionLoginController:
    def __init__(self, service: SessionAuthService):
        self._service = service

    def execute(self, email: str, password: str) -> SessionOutDto:
        session_id: str | None = self._service.create_session(email, password)
        if not session_id:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return SessionOutDto(session_id=session_id, user_id="user_id")
