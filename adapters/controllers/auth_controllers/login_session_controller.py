from fastapi import HTTPException

from application.use_cases.auth_use_cases.session_login_uc import (
    SessionLoginUseCase,
)


class SessionLoginController:
    def __init__(self, session_login_uc: SessionLoginUseCase):
        self.session_login_uc = session_login_uc

    def execute(self, email: str, password: str) -> str:
        session_id: str | None = self.session_login_uc.execute(email, password)
        if not session_id:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return session_id
