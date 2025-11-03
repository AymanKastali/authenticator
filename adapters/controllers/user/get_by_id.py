from uuid import UUID

from adapters.dto.responses.user.public import PublicUserOutDto
from application.dto.user.public import PublicUserDto
from application.use_cases.user.get_by_id import GetUserByIdUseCase


class GetUserByIdController:
    def __init__(self, use_case: GetUserByIdUseCase):
        self.use_case = use_case

    async def execute(self, user_id: UUID) -> PublicUserOutDto:
        user: PublicUserDto = await self.use_case.execute(user_id)
        return PublicUserOutDto.model_validate(user)
