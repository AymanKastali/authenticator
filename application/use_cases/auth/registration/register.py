from application.dto.auth.jwt.auth_user import AuthUserDto
from application.mappers.user import UserMapper
from domain.entities.user import UserEntity
from domain.services.user.register_user import RegisterUser
from domain.value_objects.email import EmailVo


class RegisterUserUseCase:
    def __init__(self, registration: RegisterUser):
        self._registration = registration

    async def execute(self, email: str, password: str) -> AuthUserDto:
        """
        Register a new user using the domain service.
        """
        email_vo: EmailVo = EmailVo.from_string(email)

        user: UserEntity = await self._registration.register_local_user(
            email=email_vo, plain_password=password
        )
        user.activate()

        return UserMapper.to_auth_user_dto_from_entity(user)
