from fastapi import HTTPException

from application.use_cases.auth_use_cases.session_login_uc import (
    SessionLoginUseCase,
)


class SessionLoginController:
    def __init__(self, use_case: SessionLoginUseCase):
        self.use_case = use_case

    def execute(self, email: str, password: str) -> str:
        session_id: str | None = self.use_case.execute(email, password)
        if not session_id:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return session_id
