from adapters.controllers.auth_controllers.login_jwt_controller import (
    JwtLoginController,
)
from adapters.presenters.request_models.login_user_model import LoginUserModel
from adapters.presenters.response_models.jwt_response_model import (
    JwtResponseResponseModel,
)
from adapters.presenters.response_models.success_item_response_model import (
    ItemResponseModel,
)


class JwtLoginHandler:
    def __init__(self, controller: JwtLoginController):
        self._controller = controller

    async def execute(
        self, body: LoginUserModel
    ) -> ItemResponseModel[JwtResponseResponseModel]:
        jwt_tokens: JwtResponseResponseModel = self._controller.execute(
            email=body.email, password=body.password
        )
        return ItemResponseModel[JwtResponseResponseModel].build(
            data=jwt_tokens,
            status_code=200,
            message="Login successful",
        )
