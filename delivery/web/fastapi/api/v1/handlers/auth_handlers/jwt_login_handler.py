from adapters.controllers.auth_controllers.jwt_login_controller import (
    JwtLoginController,
)
from adapters.dto.request_dto.login_user_model import LoginUserModel
from adapters.dto.response_dto.jwt_response_model import (
    JwtResponseResponseModel,
)
from adapters.dto.response_dto.success_item_response_model import (
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
            data=jwt_tokens, status_code=200, message="Login successful"
        )
