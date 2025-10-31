from adapters.dto.responses.user.registered import RegisteredUserOutDto
from application.dto.auth.jwt.auth_user import AuthUserDto
from application.use_cases.auth.registration.register import RegisterUserUseCase


class RegisterUserController:
    def __init__(self, use_case: RegisterUserUseCase):
        self.use_case = use_case

    def execute(self, email: str, password: str) -> RegisteredUserOutDto:
        user: AuthUserDto = self.use_case.execute(email, password)
        return RegisteredUserOutDto.model_validate(user)
