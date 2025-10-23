from uuid import UUID

from adapters.controllers.user_controllers.get_user_me_controller import (
    GetUserMeController,
)
from adapters.presenters.response_models.success_item_response_model import (
    ItemResponseModel,
)
from adapters.presenters.response_models.user_response_models import (
    UserResponseModel,
)


class GetUserMeHandler:
    def __init__(self, controller: GetUserMeController):
        self._controller = controller

    def execute(self, user_id: UUID) -> ItemResponseModel[UserResponseModel]:
        user: UserResponseModel = self._controller.execute(user_id)
        return ItemResponseModel[UserResponseModel].build(
            data=user,
            status_code=200,
            message="My user data retrieved successfully",
        )
