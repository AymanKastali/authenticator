from uuid import UUID

from application.dto.user.persistence import PersistenceUserDto
from application.mappers.user import UserMapper
from application.ports.repositories.user import UserRepositoryPort
from domain.entities.user import UserEntity


class AuthService:
    def __init__(self, user_repo: UserRepositoryPort):
        self._user_repo = user_repo

    def authenticate_user(self, email: str, password: str) -> UserEntity:
        """Validate user credentials and return domain entity."""
        user_dto = self._user_repo.get_user_by_email(email)
        if user_dto is None:
            raise ValueError("User not found")

        user_entity = UserMapper.to_entity_from_persistence(user_dto)
        user_entity.authenticate(password)

        return user_entity

    def get_user_by_id(self, user_id: UUID) -> UserEntity:
        """Load a user by ID."""
        user_persistence_dto: PersistenceUserDto | None = (
            self._user_repo.get_user_by_id(user_id)
        )
        if user_persistence_dto is None:
            raise ValueError("User not found")

        user: UserEntity = UserMapper.to_entity_from_persistence(
            user_persistence_dto
        )
        return user

    def get_user_by_email(self, email: str) -> UserEntity:
        """Load a user by email."""
        user_persistence_dto: PersistenceUserDto | None = (
            self._user_repo.get_user_by_email(email)
        )
        if user_persistence_dto is None:
            raise ValueError("User not found")

        user: UserEntity = UserMapper.to_entity_from_persistence(
            user_persistence_dto
        )
        return user
