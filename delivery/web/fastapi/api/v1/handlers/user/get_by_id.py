from uuid import UUID

from adapters.controllers.user.get_by_id import (
    GetUserByIdController,
)
from adapters.dto.response_dto.success_item_response_model import (
    ItemResponseModel,
)
from adapters.dto.response_dto.user_response_models import (
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
