from uuid import UUID

from adapters.dto.response_dto.user_response_models import (
    PublicUserResponseModel,
)
from application.dto.user_dto import PublicUserDto
from application.use_cases.user.get_by_id import (
    GetUserByIdUseCase,
)


class GetUserByIdController:
    def __init__(self, use_case: GetUserByIdUseCase):
        self.use_case = use_case

    def execute(self, user_id: UUID) -> PublicUserResponseModel:
        user: PublicUserDto = self.use_case.execute(user_id)
        return PublicUserResponseModel.model_validate(user)
