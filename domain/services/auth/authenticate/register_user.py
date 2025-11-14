from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import UserAlreadyExistsError
from domain.interfaces.user_factory import UserFactoryInterface
from domain.ports.repositories.user import UserRepositoryPort
from domain.services.password.hash import HashPassword
from domain.value_objects.email import EmailVo


class RegisterUser:
    """Responsible for registering new users."""

    def __init__(
        self,
        user_repo: UserRepositoryPort,
        user_factory: UserFactoryInterface,
        hasher: HashPassword,
    ):
        self._user_repo = user_repo
        self._user_factory = user_factory
        self._hasher = hasher

    async def register_local_user(
        self, email: EmailVo, plain_password: str
    ) -> UserEntity:
        existing = await self._user_repo.get_user_by_email(email)
        if existing:
            raise UserAlreadyExistsError(email.to_string())

        hashed_password = self._hasher.execute(plain_password)

        user = self._user_factory.create_local_user(
            email=email, hashed_password=hashed_password
        )
        await self._user_repo.save(user)
        return user

    async def register_external_user(self, email: EmailVo) -> UserEntity:
        existing = await self._user_repo.get_user_by_email(email)
        if existing:
            raise UserAlreadyExistsError(email.to_string())
        user = self._user_factory.create_external_user(email=email)
        await self._user_repo.save(user)
        return user
