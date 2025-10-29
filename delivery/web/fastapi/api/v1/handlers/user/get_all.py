from adapters.controllers.user.get_all import GetAllUsersController
from adapters.dto.responses.generic.success.paginated import (
    PaginatedResponseModel,
)
from adapters.dto.responses.user.public import PublicUserOutDto


class GetAllUsersHandler:
    def __init__(self, controller: GetAllUsersController):
        self._controller = controller

    def execute(
        self, page: int, page_size: int
    ) -> PaginatedResponseModel[PublicUserOutDto]:
        users: list[PublicUserOutDto] = self._controller.execute()
        return PaginatedResponseModel[PublicUserOutDto].build(
            data=users,
            status_code=200,
            message="users data retrieved successfully",
            page=page,
            per_page=page_size,
        )
