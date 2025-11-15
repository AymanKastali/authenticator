from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import UserNotFoundError
from domain.ports.repositories.user import UserRepositoryPort
from domain.value_objects.uuid_id import UUIDVo


class ManageUserStatus:
    """Responsible for managing user status."""

    def __init__(self, user_repo: UserRepositoryPort):
        self._user_repo = user_repo

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

    async def _get_user_or_raise(self, user_id: UUIDVo) -> UserEntity:
        user = await self._user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id.to_string())
        return user
