from uuid import UUID

from application.dto.user.persistence import PersistenceUserDto
from application.dto.user.public import PublicUserDto
from application.mappers.user import UserMapper
from application.ports.repositories.user import UserRepositoryPort
from domain.entities.user import UserEntity


class GetUserByIdUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    async def execute(self, user_id: UUID) -> PublicUserDto:
        dto: PersistenceUserDto | None = await self.user_repo.get_user_by_id(
            user_id
        )
        if dto is None:
            raise ValueError("UserEntity not found")

        user: UserEntity = UserMapper.to_entity_from_persistence(dto)

        if user.active is False:
            raise ValueError("User is inactive")

        user_dto: PublicUserDto = UserMapper.to_public_dto_from_entity(user)
        return user_dto
