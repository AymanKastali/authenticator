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

    async def execute(self, token: str) -> AuthenticatedUserResponseSchema:
        user_dto: TokenUserDto = await self.use_case.execute(token)
        return AuthenticatedUserResponseSchema.model_validate(user_dto)
