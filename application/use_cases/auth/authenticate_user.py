from application.ports.repositories.user import UserRepositoryPort
from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import (
    InvalidCredentialsError,
    UserDeletedError,
    UserInactiveError,
    UserNotFoundError,
)
from domain.interfaces.password_hasher import PasswordHasherInterface
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

        string_uid = user.uid.value
        if not user.is_active:
            raise UserInactiveError(string_uid)
        if user.is_deleted:
            raise UserDeletedError(string_uid)
        return user
