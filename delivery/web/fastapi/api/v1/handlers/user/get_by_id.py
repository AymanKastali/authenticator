from uuid import UUID

from adapters.controllers.user.get_by_id import GetUserByIdController
from adapters.dto.responses.generic.success.item import ItemOutDto
from adapters.dto.responses.user.public import PublicUserOutDto


class GetUserByIdHandler:
    def __init__(self, controller: GetUserByIdController):
        self._controller = controller

    def execute(self, user_id: UUID) -> ItemOutDto[PublicUserOutDto]:
        user: PublicUserOutDto = self._controller.execute(user_id)
        return ItemOutDto[PublicUserOutDto].build(
            data=user,
            status_code=200,
            message="UserEntity data retrieved successfully",
        )
