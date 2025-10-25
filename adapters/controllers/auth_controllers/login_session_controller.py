from fastapi import HTTPException

from adapters.dto.response_dto.session_response_model import (
    SessionResponseModel,
)
from application.use_cases.auth_use_cases.session_login_uc import (
    SessionLoginUseCase,
)


class SessionLoginController:
    def __init__(self, use_case: SessionLoginUseCase):
        self.use_case = use_case

    def execute(self, email: str, password: str) -> SessionResponseModel:
        session_id: str | None = self.use_case.execute(email, password)
        if not session_id:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return SessionResponseModel(session_id=session_id)
