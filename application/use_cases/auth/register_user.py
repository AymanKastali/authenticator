from application.dto.auth.jwt.auth_user import AuthUserDto
from application.mappers.user import UserMapper
from application.ports.repositories.user import UserRepositoryPort
from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import UserAlreadyExistsError
from domain.factories.value_objects.email import EmailVoFactory
from domain.factories.value_objects.hashed_password import (
    HashedPasswordVoFactory,
)
from domain.interfaces.password_hasher import PasswordHasherInterface
from domain.interfaces.policy import PolicyInterface
from domain.interfaces.user_factory import UserEntityFactoryInterface
from domain.value_objects.email import EmailVo
from domain.value_objects.role import RoleVo
from domain.value_objects.user_status import UserStatusVo


class RegisterUserUseCase:
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

    async def execute(self, email: str, plain_password: str) -> AuthUserDto:
        email_vo: EmailVo = EmailVoFactory.from_string(email)
        existing = await self._user_repo.get_user_by_email(email_vo)
        if existing:
            raise UserAlreadyExistsError(email_vo.value)

        hashed_password = self._password_factory.from_plain(
            plain=plain_password, hasher=self._hasher, policies=self._policies
        )

        user: UserEntity = self._user_factory.create(
            email=email_vo,
            hashed_password=hashed_password,
            status=UserStatusVo.ACTIVE,
            roles=[RoleVo.USER],
        )
        await self._user_repo.save(user)
        return UserMapper.to_auth_dto(user)
