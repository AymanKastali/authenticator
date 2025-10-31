from uuid import UUID

from adapters.dto.responses.auth.jwt.token_user import TokenUserOutDto
from application.dto.auth.jwt.token_user import TokenUserDto
from application.use_cases.auth.jwt.token_user import GetTokenUserUseCase


class GetTokenUserController:
    def __init__(self, use_case: GetTokenUserUseCase):
        self.use_case = use_case

    def execute(self, user_id: UUID) -> TokenUserOutDto:
        user: TokenUserDto = self.use_case.execute(user_id)
        return TokenUserOutDto.model_validate(user)
