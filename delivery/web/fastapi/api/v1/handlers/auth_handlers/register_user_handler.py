from adapters.controllers.auth_controllers.register_user_controller import (
    RegisterUserController,
)
from adapters.dto.request_dto.login_user_model import LoginUserModel
from adapters.dto.response_dto.success_item_response_model import (
    ItemResponseModel,
)
from adapters.dto.response_dto.user_response_models import (
    RegisteredUserResponseModel,
)


class RegisterUserHandler:
    def __init__(self, controller: RegisterUserController):
        self._controller = controller

    async def execute(
        self, body: LoginUserModel
    ) -> ItemResponseModel[RegisteredUserResponseModel]:
        user: RegisteredUserResponseModel = self._controller.execute(
            email=body.email, password=body.password
        )
        return ItemResponseModel[RegisteredUserResponseModel].build(
            data=user,
            status_code=201,
            message="User registered successfully",
        )
