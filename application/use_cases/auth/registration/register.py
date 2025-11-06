from application.dto.auth.jwt.auth_user import AuthUserDto
from application.mappers.user import UserMapper
from application.services.auth.registration.password_service import (
    PasswordService,
)
from domain.entities.user import UserEntity
from domain.services.user import UserDomainService
from domain.value_objects.email import EmailVo
from domain.value_objects.hashed_password import HashedPasswordVo


class RegisterUserUseCase:
    def __init__(
        self, user_service: UserDomainService, password_service: PasswordService
    ):
        self._user_service = user_service
        self._password_service = password_service

    async def execute(self, email: str, password: str) -> AuthUserDto:
        """
        Register a new user using the domain service.
        """
        email_vo: EmailVo = EmailVo.from_string(email)

        hashed_password: HashedPasswordVo = (
            self._password_service.create_hashed_password(password)
        )

        user: UserEntity = await self._user_service.register_user(
            email=email_vo,
            hashed_password=hashed_password,
        )
        user.activate()

        return UserMapper.to_auth_user_dto_from_entity(user)
