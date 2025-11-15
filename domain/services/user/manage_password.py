from domain.exceptions.domain_errors import UserNotFoundError
from domain.ports.repositories.user import UserRepositoryPort
from domain.value_objects.hashed_password import HashedPasswordVo
from domain.value_objects.uuid_id import UUIDVo


class ManageUserPassword:
    """Responsible for changing user passwords."""

    def __init__(self, user_repo: UserRepositoryPort):
        self._user_repo = user_repo

    async def change_password(
        self, user_id: UUIDVo, new_password: HashedPasswordVo
    ):
        user = await self._get_user_or_raise(user_id)
        user.change_password(new_password)
        await self._user_repo.save(user)

    async def _get_user_or_raise(self, user_id: UUIDVo):
        user = await self._user_repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id.to_string())
        return user
