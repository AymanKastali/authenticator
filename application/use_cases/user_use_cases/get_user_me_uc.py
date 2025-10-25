from uuid import UUID

from application.dto.user_dto import PersistenceUserDto, UserDto
from application.mappers.user_mapper import UserMapper
from application.ports.user_repository import UserRepositoryPort


class GetUserMeUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def execute(self, user_id: UUID) -> UserDto:
        user: PersistenceUserDto | None = self.user_repo.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        user_dto: UserDto = UserMapper.to_user_dto_from_persistence(user)
        return user_dto
