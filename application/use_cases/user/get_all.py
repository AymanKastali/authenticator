from application.dto.user.public import PublicUserDto
from application.mappers.user import UserMapper
from domain.entities.user import UserEntity
from domain.services.user import UserDomainService


class GetAllUsersUseCase:
    def __init__(self, user_service: UserDomainService):
        self._user_service = user_service

    async def execute(self) -> list[PublicUserDto]:
        users: list[UserEntity] = await self._user_service.get_all_users()

        active_users = [u for u in users if u.active]

        return [UserMapper.to_public_dto_from_entity(u) for u in active_users]
