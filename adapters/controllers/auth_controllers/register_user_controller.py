from adapters.dto.response_dto.user_response_models import (
    RegisteredUserResponseModel,
)
from application.dto.user_dto import UserDto
from application.use_cases.auth_use_cases.register_user_uc import (
    RegisterUserUseCase,
)


class RegisterUserController:
    def __init__(self, use_case: RegisterUserUseCase):
        self.use_case = use_case

    def execute(self, email: str, password: str) -> RegisteredUserResponseModel:
        user: UserDto = self.use_case.execute(email, password)
        return RegisteredUserResponseModel.model_validate(user)
