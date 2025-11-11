from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import (
    InvalidCredentialsError,
    UserDeletedError,
    UserInactiveError,
    UserNotFoundError,
)
from domain.ports.repositories.user import UserRepositoryPort
from domain.value_objects.email import EmailVo


class AuthenticateUser:
    """Responsible for authenticating users."""

    def __init__(self, user_repo: UserRepositoryPort):
        self._user_repo = user_repo

    async def authenticate_user(
        self, email: EmailVo, raw_password: str
    ) -> UserEntity:
        user = await self._user_repo.get_user_by_email(email)
        if not user:
            raise UserNotFoundError(email.to_string())
        if not user.hashed_password or not user.hashed_password.verify(
            raw_password
        ):
            raise InvalidCredentialsError(email.to_string())
        if not user.active:
            raise UserInactiveError(user.uid.to_string())
        if user.deleted:
            raise UserDeletedError(user.uid.to_string())
        return user
