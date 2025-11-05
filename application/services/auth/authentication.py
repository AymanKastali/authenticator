from uuid import UUID

from application.dto.auth.jwt.auth_user import AuthUserDto
from application.dto.user.persistence import PersistenceUserDto
from application.mappers.user import UserMapper
from application.ports.repositories.user import UserRepositoryPort
from domain.entities.user import UserEntity


class AuthService:
    def __init__(self, user_repo: UserRepositoryPort):
        self._user_repo = user_repo

    async def _load_user_entity_by_id(self, user_id: UUID) -> UserEntity:
        dto: PersistenceUserDto | None = await self._user_repo.get_user_by_id(
            user_id
        )
        if dto is None:
            raise ValueError("User not found")
        return UserMapper.to_entity_from_persistence(dto)

    async def _load_user_entity_by_email(self, email: str) -> UserEntity:
        dto: (
            PersistenceUserDto | None
        ) = await self._user_repo.get_user_by_email(email)
        if dto is None:
            raise ValueError("User not found")
        return UserMapper.to_entity_from_persistence(dto)

    async def authenticate_user(self, email: str, password: str) -> AuthUserDto:
        user: UserEntity = await self._load_user_entity_by_email(email)
        user.authenticate(password)
        return UserMapper.to_auth_user_dto_from_entity(user)

    async def get_user_by_id(self, user_id: UUID) -> AuthUserDto:
        user: UserEntity = await self._load_user_entity_by_id(user_id)
        return UserMapper.to_auth_user_dto_from_entity(user)

    async def get_user_by_email(self, email: str) -> AuthUserDto:
        user: UserEntity = await self._load_user_entity_by_email(email)
        return UserMapper.to_auth_user_dto_from_entity(user)
