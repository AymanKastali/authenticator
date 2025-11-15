from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import UserAlreadyExistsError
from domain.factories.value_objects.hashed_password import (
    HashedPasswordVoFactory,
)
from domain.interfaces.password_hasher import PasswordHasherInterface
from domain.interfaces.policy import PolicyInterface
from domain.interfaces.user_factory import UserEntityFactoryInterface
from domain.ports.repositories.user import UserRepositoryPort
from domain.value_objects.email import EmailVo
from domain.value_objects.role import RoleVo
from domain.value_objects.user_status import UserStatusVo


class RegisterUser:
    """Responsible for registering new users."""

    def __init__(
        self,
        user_repo: UserRepositoryPort,
        user_factory: UserEntityFactoryInterface,
        hasher: PasswordHasherInterface,
        policies: list[PolicyInterface],
    ):
        self._user_repo = user_repo
        self._user_factory = user_factory
        self._password_factory = HashedPasswordVoFactory()
        self._hasher = hasher
        self._policies = policies

    async def execute(self, email: EmailVo, plain_password: str) -> UserEntity:
        existing = await self._user_repo.get_user_by_email(email)
        if existing:
            raise UserAlreadyExistsError(email.value)

        hashed_password = self._password_factory.from_plain(
            plain=plain_password, hasher=self._hasher, policies=self._policies
        )

        user: UserEntity = self._user_factory.create(
            email=email,
            hashed_password=hashed_password,
            status=UserStatusVo.ACTIVE,
            roles=[RoleVo.USER],
        )
        await self._user_repo.save(user)
        return user
