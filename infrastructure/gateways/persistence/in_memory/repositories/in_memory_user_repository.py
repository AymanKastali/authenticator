from uuid import UUID

from domain.entities.user import UserEntity
from domain.ports.repositories.user import UserRepositoryPort
from domain.value_objects.email import EmailVo
from domain.value_objects.identifiers import UUIDVo


class InMemoryUserRepository(UserRepositoryPort):
    def __init__(self):
        self.users: dict[UUID, UserEntity] = {}

    async def save(self, user: UserEntity) -> None:
        self.users[user.uid.to_uuid()] = user

    async def get_user_by_id(self, user_id: UUIDVo) -> UserEntity | None:
        return self.users.get(user_id.to_uuid())

    async def get_user_by_email(self, email: EmailVo) -> UserEntity | None:
        user = next((u for u in self.users.values() if u.email == email), None)
        return user

    async def get_all_users(self) -> list[UserEntity]:
        return list(self.users.values())
