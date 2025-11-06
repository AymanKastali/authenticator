from uuid import UUID

from application.dto.auth.jwt.token_user import TokenUserDto
from application.use_cases.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserUseCase,
)
from presentation.web.fastapi.schemas.response.auth.jwt.authenticated_user import (
    AuthenticatedUserResponseSchema,
)


class GetAuthenticatedUserController:
    def __init__(self, use_case: GetAuthenticatedUserUseCase):
        self.use_case = use_case

    async def execute(self, user_id: UUID) -> AuthenticatedUserResponseSchema:
        user: TokenUserDto = await self.use_case.execute(user_id)
        return AuthenticatedUserResponseSchema.model_validate(user)
