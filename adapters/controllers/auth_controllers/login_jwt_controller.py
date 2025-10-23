from fastapi import HTTPException

from adapters.presenters.response_models.jwt_response_model import (
    JwtResponseResponseModel,
)
from application.use_cases.auth_use_cases.jwt_login_uc import JwtLoginUseCase


class JwtLoginController:
    def __init__(self, use_case: JwtLoginUseCase):
        self.use_case = use_case

    def execute(self, email: str, password: str) -> JwtResponseResponseModel:
        jwt_tokens: dict = self.use_case.execute(email, password)
        if not jwt_tokens:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return JwtResponseResponseModel(**jwt_tokens)
