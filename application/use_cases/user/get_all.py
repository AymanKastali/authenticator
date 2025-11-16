from application.dto.user.public import PublicUserDto
from application.mappers.user import UserMapper
from application.services.user import UserQueryService
from domain.entities.user import UserEntity


class GetAllUsersUseCase:
    def __init__(self, user_query_service: UserQueryService):
        self._user_query_service = user_query_service

    async def execute(self) -> list[PublicUserDto]:
        users: list[UserEntity] = await self._user_query_service.get_all_users()

        active_users = [u for u in users if u.is_active]

        return [UserMapper.to_public_dto(u) for u in active_users]
