from uuid import UUID

from application.dto.auth.jwt.token_user import TokenUserDto
from application.dto.user.persistence import PersistenceUserDto
from application.mappers.user import UserMapper
from application.ports.repositories.user import UserRepositoryPort


class GetTokenUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def execute(self, user_id: UUID) -> TokenUserDto:
        user: PersistenceUserDto | None = self.user_repo.get_user_by_id(user_id)
        if user is None:
            raise ValueError("UserEntity not found")

        user_dto: TokenUserDto = (
            UserMapper.to_token_user_dto_from_persistence_dto(user)
        )
        return user_dto
