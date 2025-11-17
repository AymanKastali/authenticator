from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import (
    InvalidCredentialsError,
    UserNotFoundError,
)
from domain.interfaces.password_hasher import PasswordHasherInterface
from domain.ports.repositories.user import UserRepositoryPort
from domain.value_objects.email import EmailVo
from domain.value_objects.hashed_password import HashedPasswordVo


class AuthenticateUserUseCase:
    """Responsible for authenticating users."""

    def __init__(
        self,
        user_repo: UserRepositoryPort,
        password_hasher: PasswordHasherInterface,
    ):
        self._user_repo = user_repo
        self._password_hasher = password_hasher

    async def authenticate_user(
        self, email: EmailVo, raw_password: str
    ) -> UserEntity:
        user: UserEntity | None = await self._user_repo.get_user_by_email(email)
        string_email = email.value

        if user is None:
            raise UserNotFoundError(email.value)

        hashed_password: HashedPasswordVo | None = user.hashed_password
        if hashed_password is None:
            raise InvalidCredentialsError(string_email)

        if (
            self._password_hasher.verify(
                password=raw_password, hashed=hashed_password
            )
            is False
        ):
            raise InvalidCredentialsError(string_email)

        user.ensure_active()
        user.ensure_not_deleted()
        return user
