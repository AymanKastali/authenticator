from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserDeletedError,
    UserInactiveError,
    UserNotFoundError,
)
from domain.ports.repositories.user import UserRepositoryPort
from domain.value_objects.email import EmailVo
from domain.value_objects.hashed_password import HashedPasswordVo
from domain.value_objects.identifiers import UUIDVo


class UserDomainService:
    """Orchestrates operations on UserEntity that involve repositories or external concerns."""

    def __init__(self, user_repo: UserRepositoryPort):
        self._user_repo = user_repo

    # ----------------- Registration / Creation -----------------
    async def register_user(
        self, email: EmailVo, hashed_password: HashedPasswordVo
    ) -> UserEntity:
        existing = await self._user_repo.get_user_by_email(email)
        if existing:
            raise UserAlreadyExistsError(email.to_string())

        user = UserEntity.create_local(
            email=email, hashed_password=hashed_password
        )
        await self._user_repo.save(user)
        return user

    async def create_external_user(self, email: EmailVo) -> UserEntity:
        existing = await self._user_repo.get_user_by_email(email)
        if existing:
            raise UserAlreadyExistsError(email.to_string())

        user = UserEntity.create_external(email=email)
        await self._user_repo.save(user)
        return user

    # ----------------- Authentication -----------------
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

    # ----------------- Status Management -----------------
    async def activate_user(self, user_id: UUIDVo):
        user = await self._get_user_or_raise(user_id)
        user.activate()
        await self._user_repo.save(user)

    async def deactivate_user(self, user_id: UUIDVo):
        user = await self._get_user_or_raise(user_id)
        user.deactivate()
        await self._user_repo.save(user)

    async def mark_user_verified(self, user_id: UUIDVo):
        user = await self._get_user_or_raise(user_id)
        user.mark_verified()
        await self._user_repo.save(user)

    # ----------------- Password Management -----------------
    async def change_user_password(
        self, user_id: UUIDVo, new_password: HashedPasswordVo
    ):
        user = await self._get_user_or_raise(user_id)
        user.change_password(new_password)
        await self._user_repo.save(user)

    # ----------------- Helpers -----------------
    async def _get_user_or_raise(self, user_id: UUIDVo) -> UserEntity:
        user = await self._user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id.to_string())
        return user

    # ------------------------------------
    async def get_user_by_email(self, email: EmailVo) -> UserEntity | None:
        """Fetch a user by email. Returns None if not found."""
        return await self._user_repo.get_user_by_email(email)

    async def get_user_by_id(self, user_id: UUIDVo) -> UserEntity | None:
        """Fetch a user by ID. Returns None if not found."""
        return await self._user_repo.get_user_by_id(user_id)

    async def get_all_users(self) -> list[UserEntity]:
        return await self._user_repo.get_all_users()
