from adapters.controllers.user.get_all import GetAllUsersController
from adapters.dto.responses.generic.success.paginated import (
    PaginatedResponseModel,
)
from adapters.dto.responses.user.public import PublicUserOutDto
from application.ports.services.logger import LoggerPort


class GetAllUsersHandler:
    def __init__(self, controller: GetAllUsersController, logger: LoggerPort):
        self._controller = controller
        self._logger = logger

    async def execute(
        self, page: int, page_size: int
    ) -> PaginatedResponseModel[PublicUserOutDto]:
        self._logger.info(
            f"[GetAllUsersHandler] Retrieving users list: page={page}, page_size={page_size}"
        )
        users: list[PublicUserOutDto] = await self._controller.execute()
        self._logger.info(
            f"[GetAllUsersHandler] Successfully retrieved {len(users)} users: page={page}, page_size={page_size}"
        )
        return PaginatedResponseModel[PublicUserOutDto].build(
            data=users,
            status_code=200,
            message="users data retrieved successfully",
            page=page,
            per_page=page_size,
        )
