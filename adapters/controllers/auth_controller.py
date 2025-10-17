from fastapi import HTTPException

from application.use_cases.login_user import LoginUserUseCase


class AuthController:
    def __init__(self, login_use_case: LoginUserUseCase):
        self.login_use_case = login_use_case

    def login(self, email: str, password: str) -> dict:
        result = self.login_use_case.execute(email, password)
        if not result:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return result
