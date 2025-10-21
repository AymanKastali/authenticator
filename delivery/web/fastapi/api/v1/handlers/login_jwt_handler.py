from adapters.controllers.login_jwt_controller import JwtLoginController
from adapters.presenters.request_models.login_user_model import LoginUserModel
from adapters.presenters.response_models.success_item_response_model import (
    ItemResponseModel,
)


class JwtLoginHandler:
    def __init__(self, controller: JwtLoginController):
        self._controller = controller

    async def execute(self, body: LoginUserModel) -> ItemResponseModel[dict]:
        jwt_tokens: dict = self._controller.execute(
            email=body.email, password=body.password
        )
        return ItemResponseModel[dict].build(
            data=jwt_tokens,
            status_code=200,
            message="Login successful",
        )
