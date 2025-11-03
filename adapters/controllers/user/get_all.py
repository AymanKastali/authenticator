from adapters.dto.responses.user.public import PublicUserOutDto
from application.dto.user.public import PublicUserDto
from application.use_cases.user.get_all import GetAllUsersUseCase


class GetAllUsersController:
    def __init__(self, use_case: GetAllUsersUseCase):
        self.use_case = use_case

    async def execute(self) -> list[PublicUserOutDto]:
        users: list[PublicUserDto] = await self.use_case.execute()
        return [PublicUserOutDto.model_validate(user) for user in users]
