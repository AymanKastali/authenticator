from uuid import UUID

from adapters.controllers.auth.jwt.me import ReadMeController
from adapters.dto.responses.auth.jwt.me import ReadMeOutDto
from adapters.dto.responses.generic.success.item import ItemOutDto


class ReadMeHandler:
    def __init__(self, controller: ReadMeController):
        self._controller = controller

    def execute(self, user_id: UUID) -> ItemOutDto[ReadMeOutDto]:
        user: ReadMeOutDto = self._controller.execute(user_id)
        return ItemOutDto[ReadMeOutDto].build(
            data=user,
            status_code=200,
            message="My user data retrieved successfully",
        )
