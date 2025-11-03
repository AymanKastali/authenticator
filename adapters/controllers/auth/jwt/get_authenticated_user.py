from uuid import UUID

from adapters.dto.responses.auth.jwt.authenticated_user import (
    AuthenticatedUserOutDto,
)
from application.dto.auth.jwt.token_user import TokenUserDto
from application.use_cases.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserUseCase,
)


class GetAuthenticatedUserController:
    def __init__(self, use_case: GetAuthenticatedUserUseCase):
        self.use_case = use_case

    async def execute(self, user_id: UUID) -> AuthenticatedUserOutDto:
        user: TokenUserDto = await self.use_case.execute(user_id)
        return AuthenticatedUserOutDto.model_validate(user)
