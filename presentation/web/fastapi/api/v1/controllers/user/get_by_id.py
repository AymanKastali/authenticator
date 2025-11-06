from uuid import UUID

from application.dto.user.public import PublicUserDto
from application.ports.services.logger import LoggerPort
from application.use_cases.user.get_by_id import GetUserByIdUseCase
from presentation.web.fastapi.schemas.response.generic.success.item import (
    ItemResponseSchema,
)
from presentation.web.fastapi.schemas.response.user.public import (
    PublicUserResponseSchema,
)


class GetUserByIdController:
    def __init__(self, use_case: GetUserByIdUseCase, logger: LoggerPort):
        self._use_case = use_case
        self._logger = logger

    async def execute(
        self, user_id: UUID
    ) -> ItemResponseSchema[PublicUserResponseSchema]:
        self._logger.info(
            f"[GetUserByIdController] Retrieving user data for user_id={user_id}"
        )
        dto: PublicUserDto = await self._use_case.execute(user_id)
        user = PublicUserResponseSchema.model_validate(dto)
        self._logger.info(
            f"[GetUserByIdController] Successfully retrieved data for user_id={user_id}"
        )
        return ItemResponseSchema[PublicUserResponseSchema].build(
            data=user,
            status_code=200,
            message="UserEntity data retrieved successfully",
        )
