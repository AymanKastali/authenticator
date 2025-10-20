from adapters.presenters.response_models.user_response_models import (
    RegisteredUserResponseModel,
)
from application.dto.user_dto import UserDTO
from application.use_cases.register_user import RegisterUserUseCase


class RegisterUserController:
    def __init__(self, register_user_uc: RegisterUserUseCase):
        self.register_user_uc = register_user_uc

    def execute(self, email_address: str, password: str) -> dict:
        user: UserDTO = self.register_user_uc.execute(email_address, password)
        return RegisteredUserResponseModel.model_validate(user).model_dump()
