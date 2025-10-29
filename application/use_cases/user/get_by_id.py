from uuid import UUID

from application.dto.user.persistence import PersistenceUserDto
from application.dto.user.public import PublicUserDto
from application.mappers.user import UserMapper
from application.ports.repositories.user import UserRepositoryPort


class GetUserByIdUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def execute(self, user_id: UUID) -> PublicUserDto:
        user: PersistenceUserDto | None = self.user_repo.get_user_by_id(user_id)
        if user is None:
            raise ValueError("UserEntity not found")

        user_dto: PublicUserDto = UserMapper.to_public_dto_from_persistence(
            user
        )
        return user_dto
