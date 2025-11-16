from application.dto.auth.jwt.token_user import TokenUserDto
from application.services.jwt.get_authenticated_user import (
    GetJwtAuthenticatedUserService,
)
from presentation.web.fastapi.schemas.response.auth.jwt.authenticated_user import (
    AuthenticatedUserResponseSchema,
)


class GetAuthenticatedUserController:
    def __init__(self, service: GetJwtAuthenticatedUserService):
        self.service = service

    async def execute(self, token: str) -> AuthenticatedUserResponseSchema:
        user_dto: TokenUserDto = await self.service.execute(token)
        return AuthenticatedUserResponseSchema.model_validate(user_dto)
