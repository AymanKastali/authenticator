from adapters.controllers.auth_controllers.register_user_controller import (
    RegisterUserController,
)
from adapters.presenters.request_models.login_user_model import LoginUserModel
from adapters.presenters.response_models.success_item_response_model import (
    ItemResponseModel,
)


class RegisterUserHandler:
    def __init__(self, controller: RegisterUserController):
        self._controller = controller

    async def execute(self, body: LoginUserModel) -> ItemResponseModel[dict]:
        user: dict = self._controller.execute(
            email=body.email, password=body.password
        )
        return ItemResponseModel[dict].build(
            data=user,
            status_code=201,
            message="User registered successfully",
        )
