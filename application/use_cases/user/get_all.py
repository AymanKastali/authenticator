from application.dto.user.public import PublicUserDto
from application.mappers.user import UserMapper
from domain.entities.user import UserEntity
from domain.ports.repositories.user import UserRepositoryPort


class GetAllUsersUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self._user_repo = user_repo

    async def execute(self) -> list[PublicUserDto]:
        users: list[UserEntity] = await self._user_repo.get_all_users()

        active_users = [u for u in users if u.is_active]

        return [UserMapper.to_public_dto(u) for u in active_users]
