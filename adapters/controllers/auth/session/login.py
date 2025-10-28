from fastapi import HTTPException

from adapters.dto.response_dto.session_response_dto import SessionOutDto
from application.use_cases.auth.session.login import (
    SessionLoginUseCase,
)


class SessionLoginController:
    def __init__(self, use_case: SessionLoginUseCase):
        self.use_case = use_case

    def execute(self, email: str, password: str) -> SessionOutDto:
        session_id: str | None = self.use_case.execute(email, password)
        if not session_id:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return SessionOutDto(session_id=session_id, user_id=user_id)
