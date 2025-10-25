from uuid import UUID

from adapters.dto.response_dto.user_response_models import (
    AuthenticatedUserResponseModel,
)
from application.dto.user_dto import UserDto
from application.use_cases.user_use_cases.get_request_user_uc import (
    GetRequestUserUseCase,
)


class GetRequestUserController:
    def __init__(self, use_case: GetRequestUserUseCase):
        self.use_case = use_case

    def execute(self, user_id: UUID) -> AuthenticatedUserResponseModel:
        user: UserDto = self.use_case.execute(user_id)
        return AuthenticatedUserResponseModel.model_validate(user)
