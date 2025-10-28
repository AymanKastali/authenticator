from uuid import UUID

from adapters.controllers.user.get_me import (
    GetRequestUserController,
)
from adapters.dto.response_dto.success_item_response_model import (
    ItemResponseModel,
)
from adapters.dto.response_dto.user_response_models import (
    UserResponseModel,
)


class GetRequestUserHandler:
    def __init__(self, controller: GetRequestUserController):
        self._controller = controller

    def execute(self, user_id: UUID) -> ItemResponseModel[UserResponseModel]:
        user: UserResponseModel = self._controller.execute(user_id)
        return ItemResponseModel[UserResponseModel].build(
            data=user,
            status_code=200,
            message="My user data retrieved successfully",
        )
