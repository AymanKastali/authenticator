from application.dto.user.public import PublicUserDto
from application.mappers.user import UserMapper
from application.repositories.user import UserRepository
from domain.entities.user import UserEntity


class GetAllUsersUseCase:
    def __init__(self, user_repo: UserRepository):
        self._query_user = user_repo

    async def execute(self) -> list[PublicUserDto]:
        users: list[UserEntity] = await self._query_user.get_all_users()

        active_users = [u for u in users if u.is_active]

        return [UserMapper.to_public_dto(u) for u in active_users]
