from adapters.controllers.user_controllers.get_all_users_controller import (
    GetAllUsersController,
)
from adapters.dto.response_dto.success_paginated_response_model import (
    PaginatedResponseModel,
)
from adapters.dto.response_dto.user_response_models import (
    PublicUserResponseModel,
)


class GetAllUsersHandler:
    def __init__(self, controller: GetAllUsersController):
        self._controller = controller

    def execute(self) -> PaginatedResponseModel[PublicUserResponseModel]:
        users: list[PublicUserResponseModel] = self._controller.execute()
        return PaginatedResponseModel[PublicUserResponseModel].build(
            data=users,
            status_code=200,
            message="users data retrieved successfully",
        )
