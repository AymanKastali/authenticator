from uuid import UUID

from adapters.presenters.response_models.user_response_models import (
    UserResponseModel,
)
from application.dto.user_dto.user_dto import UserDTO
from application.use_cases.user_use_cases.get_user_me_uc import GetUserMeUseCase


class GetUserMeController:
    def __init__(self, use_case: GetUserMeUseCase):
        self.use_case = use_case

    def execute(self, user_id: UUID) -> dict:
        user: UserDTO = self.use_case.execute(user_id)
        return UserResponseModel.model_validate(user).model_dump()
