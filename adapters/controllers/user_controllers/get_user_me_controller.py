from uuid import UUID

from adapters.dto.response_dto.user_response_models import (
    UserResponseModel,
)
from application.dto.user_dto import UserDto
from application.use_cases.user_use_cases.get_user_me_uc import GetUserMeUseCase


class GetUserMeController:
    def __init__(self, use_case: GetUserMeUseCase):
        self.use_case = use_case

    def execute(self, user_id: UUID) -> UserResponseModel:
        user: UserDto = self.use_case.execute(user_id)
        return UserResponseModel.model_validate(user)
