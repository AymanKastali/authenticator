from uuid import UUID

from application.dto.auth.jwt.token_user import TokenUserDto
from application.dto.user.persistence import PersistenceUserDto
from application.mappers.user import UserMapper
from application.ports.repositories.user import UserRepositoryPort
from domain.entities.user import UserEntity


class GetAuthenticatedUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    async def execute(self, user_id: UUID) -> TokenUserDto:
        dto: PersistenceUserDto | None = await self.user_repo.get_user_by_id(
            user_id
        )
        if dto is None:
            raise ValueError("User not found")

        user: UserEntity = UserMapper.to_entity_from_persistence(dto)

        if user.deleted:
            raise ValueError("User deleted")

        user_dto: TokenUserDto = UserMapper.to_token_user_dto_from_entity(user)
        return user_dto
