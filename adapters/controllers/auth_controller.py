from fastapi import HTTPException

from adapters.presenters.logged_in_user_presenter import LoggedInUserPresenter
from application.dto.logged_in_user_dto import LoggedInUserDTO
from application.use_cases.login_user_use_case import LoginUserUseCase


class AuthController:
    def __init__(self, login_use_case: LoginUserUseCase):
        self.login_use_case = login_use_case

    def login(self, email: str, password: str) -> dict:
        result: LoggedInUserDTO | None = self.login_use_case.execute(
            email, password
        )
        if not result:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return LoggedInUserPresenter.to_json(result)
