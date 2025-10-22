from uuid import UUID

from adapters.controllers.user_controllers.get_user_by_id_controller import (
    GetUserByIdController,
)
from adapters.presenters.response_models.success_item_response_model import (
    ItemResponseModel,
)


class GetUserByIdHandler:
    def __init__(self, controller: GetUserByIdController):
        self._controller = controller

    def execute(self, user_id: UUID) -> ItemResponseModel[dict]:
        user: dict = self._controller.execute(user_id)
        return ItemResponseModel[dict].build(
            data=user,
            status_code=200,
            message="User data retrieved successfully",
        )
