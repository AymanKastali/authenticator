from adapters.controllers.user_controllers.get_all_users_controller import (
    GetAllUsersController,
)
from adapters.presenters.response_models.success_paginated_response_model import (
    PaginatedResponseModel,
)


class GetAllUsersHandler:
    def __init__(self, controller: GetAllUsersController):
        self._controller = controller

    def execute(self) -> PaginatedResponseModel[dict]:
        users: list[dict] = self._controller.execute()
        return PaginatedResponseModel[dict].build(
            data=users,
            status_code=200,
            message="users data retrieved successfully",
        )
