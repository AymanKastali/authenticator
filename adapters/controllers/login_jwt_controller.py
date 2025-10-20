from fastapi import HTTPException

from adapters.presenters.response_models.jwt_response_model import (
    JwtResponseResponseModel,
)
from application.use_cases.jwt_login import JwtLoginUseCase


class JwtLoginController:
    def __init__(self, jwt_login_uc: JwtLoginUseCase):
        self.jwt_login_uc = jwt_login_uc

    def execute(self, email_address: str, password: str) -> dict:
        jwt_tokens: dict = self.jwt_login_uc.execute(email_address, password)
        if not jwt_tokens:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return JwtResponseResponseModel(**jwt_tokens).model_dump()
