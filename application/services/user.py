from application.ports.repositories.user import UserRepositoryPort
from domain.entities.user import UserEntity
from domain.value_objects.email import EmailVo
from domain.value_objects.uuid_id import UUIDVo


class UserQueryService:
    """Responsible for fetching users."""

    def __init__(self, user_repo: UserRepositoryPort):
        self._user_repo = user_repo

    async def get_user_by_email(self, email: EmailVo) -> UserEntity | None:
        return await self._user_repo.get_user_by_email(email)

    async def get_user_by_id(self, user_id: UUIDVo) -> UserEntity | None:
        return await self._user_repo.get_user_by_id(user_id)

    async def get_all_users(self) -> list[UserEntity]:
        return await self._user_repo.get_all_users()
