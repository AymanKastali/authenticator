from adapters.controllers.auth_controller import AuthController
from adapters.request_models.login_user_model import LoginUserModel


class LoginUserHandler:
    def __init__(self, controller: AuthController):
        self._controller = controller

    async def handle(self, body: LoginUserModel) -> dict:
        user_dto: dict = self._controller.login(
            email=body.email, password=body.password
        )
        return user_dto
