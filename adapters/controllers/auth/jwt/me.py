from uuid import UUID

from adapters.dto.responses.auth.jwt.me import ReadMeOutDto
from application.dto.user.me import CurrentUserDto
from application.use_cases.auth.jwt.me import ReadMeUseCase


class ReadMeController:
    def __init__(self, use_case: ReadMeUseCase):
        self.use_case = use_case

    def execute(self, user_id: UUID) -> ReadMeOutDto:
        user: CurrentUserDto = self.use_case.execute(user_id)
        return ReadMeOutDto.model_validate(user)
