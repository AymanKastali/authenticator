from uuid import UUID

from application.ports.repositories.user import UserRepositoryPort
from domain.entities.user import UserEntity
from domain.value_objects.email import EmailVo
from domain.value_objects.uuid_id import UUIDVo
from infrastructure.gateways.persistence.in_memory.db.storage import (
    InMemoryUserStorage,
)


class InMemoryUserRepository(UserRepositoryPort):
    def __init__(self, storage: InMemoryUserStorage):
        self._storage = storage

    async def save(self, user: UserEntity) -> None:
        self._storage.users[UUID(user.uid.value)] = user

    async def get_user_by_id(self, user_id: UUIDVo) -> UserEntity | None:
        return self._storage.users.get(UUID(user_id.value))

    async def get_user_by_email(self, email: EmailVo) -> UserEntity | None:
        user = next(
            (u for u in self._storage.users.values() if u.email == email), None
        )
        return user

    async def get_all_users(self) -> list[UserEntity]:
        return list(self._storage.users.values())
