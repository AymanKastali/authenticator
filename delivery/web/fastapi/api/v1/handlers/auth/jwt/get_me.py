from uuid import UUID

from adapters.controllers.auth.jwt.me import ReadMeController
from adapters.dto.responses.auth.jwt.me import ReadMeOutDto
from adapters.dto.responses.generic.success.item import ItemOutDto
from application.ports.services.logger import LoggerPort


class ReadMeHandler:
    def __init__(self, controller: ReadMeController, logger: LoggerPort):
        self._controller = controller
        self._logger = logger

    def execute(self, user_id: UUID) -> ItemOutDto[ReadMeOutDto]:
        self._logger.info(
            f"[ReadMeHandler] Fetching user data for user_id={user_id}"
        )
        user: ReadMeOutDto = self._controller.execute(user_id)
        self._logger.info(
            f"[ReadMeHandler] Successfully retrieved user data for user_id={user_id}"
        )
        return ItemOutDto[ReadMeOutDto].build(
            data=user,
            status_code=200,
            message="My user data retrieved successfully",
        )
