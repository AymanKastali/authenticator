from uuid import UUID

from adapters.controllers.user_controllers.get_user_by_id_controller import (
    GetUserByIdController,
)
from adapters.presenters.response_models.success_item_response_model import (
    ItemResponseModel,
)
from adapters.presenters.response_models.user_response_models import (
    PublicUserResponseModel,
)


class GetUserByIdHandler:
    def __init__(self, controller: GetUserByIdController):
        self._controller = controller

    def execute(
        self, user_id: UUID
    ) -> ItemResponseModel[PublicUserResponseModel]:
        user: PublicUserResponseModel = self._controller.execute(user_id)
        return ItemResponseModel[PublicUserResponseModel].build(
            data=user,
            status_code=200,
            message="User data retrieved successfully",
        )
