from application.dto.user.public import PublicUserDto
from application.mappers.user import UserMapper
from domain.entities.user import UserEntity
from domain.services.user.query_user import QueryUser


class GetAllUsersUseCase:
    def __init__(self, query_user: QueryUser):
        self._query_user = query_user

    async def execute(self) -> list[PublicUserDto]:
        users: list[UserEntity] = await self._query_user.get_all_users()

        active_users = [u for u in users if u.is_active]

        return [UserMapper.to_public_dto_from_entity(u) for u in active_users]
