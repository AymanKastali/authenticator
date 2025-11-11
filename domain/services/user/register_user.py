from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import UserAlreadyExistsError
from domain.interfaces.policy import PolicyInterface
from domain.ports.repositories.user import UserRepositoryPort
from domain.value_objects.email import EmailVo
from domain.value_objects.hashed_password import HashedPasswordVo


class RegisterUser:
    """Responsible for registering new users."""

    def __init__(
        self,
        user_repo: UserRepositoryPort,
        password_policies: list[PolicyInterface],
    ):
        self._user_repo = user_repo
        self._password_policies = password_policies

    async def register_local_user(
        self, email: EmailVo, plain_password: str
    ) -> UserEntity:
        existing = await self._user_repo.get_user_by_email(email)
        if existing:
            raise UserAlreadyExistsError(email.to_string())

        hashed_password = HashedPasswordVo.create(
            plain_password, self._password_policies
        )
        user = UserEntity.create_local(
            email=email, hashed_password=hashed_password
        )
        await self._user_repo.save(user)
        return user

    async def register_external_user(self, email: EmailVo) -> UserEntity:
        existing = await self._user_repo.get_user_by_email(email)
        if existing:
            raise UserAlreadyExistsError(email.to_string())
        user = UserEntity.create_external(email=email)
        await self._user_repo.save(user)
        return user
