from application.dto.user.public import PublicUserDto
from application.ports.services.logger import LoggerPort
from application.use_cases.user.get_all import GetAllUsersUseCase
from presentation.web.fastapi.schemas.response.generic.success.paginated import (
    PaginatedResponseModel,
)
from presentation.web.fastapi.schemas.response.user.public import (
    PublicUserResponseSchema,
)


class GetAllUsersController:
    def __init__(self, use_case: GetAllUsersUseCase, logger: LoggerPort):
        self._use_case = use_case
        self._logger = logger

    async def execute(
        self, page: int, page_size: int
    ) -> PaginatedResponseModel[PublicUserResponseSchema]:
        self._logger.info(
            f"[GetAllUsersController] Retrieving users list: page={page}, page_size={page_size}"
        )
        dto_list: list[PublicUserDto] = await self._use_case.execute()
        users = [
            PublicUserResponseSchema.model_validate(dto) for dto in dto_list
        ]
        self._logger.info(
            f"[GetAllUsersController] Successfully retrieved {len(dto_list)} users: page={page}, page_size={page_size}"
        )
        return PaginatedResponseModel[PublicUserResponseSchema].build(
            data=users,
            status_code=200,
            message="users data retrieved successfully",
            page=page,
            per_page=page_size,
        )
