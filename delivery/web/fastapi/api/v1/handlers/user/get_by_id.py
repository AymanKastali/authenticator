from uuid import UUID

from adapters.controllers.user.get_by_id import GetUserByIdController
from adapters.dto.responses.generic.success.item import ItemOutDto
from adapters.dto.responses.user.public import PublicUserOutDto
from application.ports.services.logger import LoggerPort


class GetUserByIdHandler:
    def __init__(self, controller: GetUserByIdController, logger: LoggerPort):
        self._controller = controller
        self._logger = logger

    def execute(self, user_id: UUID) -> ItemOutDto[PublicUserOutDto]:
        self._logger.info(
            f"[GetUserByIdHandler] Retrieving user data for user_id={user_id}"
        )
        user: PublicUserOutDto = self._controller.execute(user_id)
        self._logger.info(
            f"[GetUserByIdHandler] Successfully retrieved data for user_id={user_id}"
        )
        return ItemOutDto[PublicUserOutDto].build(
            data=user,
            status_code=200,
            message="UserEntity data retrieved successfully",
        )
