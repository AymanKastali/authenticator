from adapters.dto.response_dto.user_response_models import (
    PublicUserResponseModel,
)
from application.dto.user_dto import PublicUserDto
from application.use_cases.user_use_cases.get_all_users_uc import (
    GetAllUsersUseCase,
)


class GetAllUsersController:
    def __init__(self, use_case: GetAllUsersUseCase):
        self.use_case = use_case

    def execute(self) -> list[PublicUserResponseModel]:
        users: list[PublicUserDto] = self.use_case.execute()
        return [PublicUserResponseModel.model_validate(user) for user in users]
