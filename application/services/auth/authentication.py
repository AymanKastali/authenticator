from uuid import UUID

from application.dto.user.persistence import PersistenceUserDto
from application.mappers.user import UserMapper
from application.ports.repositories.user import UserRepositoryPort


class AuthService:
    def __init__(self, user_repo: UserRepositoryPort):
        self._user_repo = user_repo

    async def authenticate_user(
        self, email: str, password: str
    ) -> PersistenceUserDto:
        """Validate user credentials and return domain entity."""
        user_persistence_dto = await self._user_repo.get_user_by_email(email)
        if user_persistence_dto is None:
            raise ValueError("User not found")

        user_entity = UserMapper.to_entity_from_persistence(
            user_persistence_dto
        )
        user_entity.authenticate(password)

        return user_persistence_dto

    async def get_user_by_id(self, user_id: UUID) -> PersistenceUserDto:
        """Load a user by ID."""
        user_persistence_dto: (
            PersistenceUserDto | None
        ) = await self._user_repo.get_user_by_id(user_id)
        if user_persistence_dto is None:
            raise ValueError("User not found")

        _ = UserMapper.to_entity_from_persistence(user_persistence_dto)
        return user_persistence_dto

    async def get_user_by_email(self, email: str) -> PersistenceUserDto:
        """Load a user by email."""
        user_persistence_dto: (
            PersistenceUserDto | None
        ) = await self._user_repo.get_user_by_email(email)
        if user_persistence_dto is None:
            raise ValueError("User not found")

        _ = UserMapper.to_entity_from_persistence(user_persistence_dto)
        return user_persistence_dto
