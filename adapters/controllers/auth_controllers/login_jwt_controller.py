from fastapi import HTTPException

from adapters.presenters.response_models.jwt_response_model import (
    JwtResponseResponseModel,
)
from application.use_cases.auth_use_cases.jwt_login_uc import JwtLoginUseCase


class JwtLoginController:
    def __init__(self, jwt_login_uc: JwtLoginUseCase):
        self.jwt_login_uc = jwt_login_uc

    def execute(self, email: str, password: str) -> dict:
        jwt_tokens: dict = self.jwt_login_uc.execute(email, password)
        if not jwt_tokens:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return JwtResponseResponseModel(**jwt_tokens).model_dump()
