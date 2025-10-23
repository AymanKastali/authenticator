from uuid import UUID

from adapters.presenters.response_models.user_response_models import (
    PublicUserResponseModel,
)
from application.dto.user_dto.public_user_dto import PublicUserDTO
from application.use_cases.user_use_cases.get_user_by_id_uc import (
    GetUserByIdUseCase,
)


class GetUserByIdController:
    def __init__(self, use_case: GetUserByIdUseCase):
        self.use_case = use_case

    def execute(self, user_id: UUID) -> PublicUserResponseModel:
        user: PublicUserDTO = self.use_case.execute(user_id)
        return PublicUserResponseModel.model_validate(user)
