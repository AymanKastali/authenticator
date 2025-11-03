from uuid import UUID

from application.dto.user.persistence import PersistenceUserDto
from application.ports.repositories.user import UserRepositoryPort


class InMemoryUserRepository(UserRepositoryPort):
    def __init__(self):
        self.users: dict[str, PersistenceUserDto] = {}

    async def save(self, user: PersistenceUserDto) -> None:
        self.users[user.uid] = user

    async def get_user_by_id(self, user_id: UUID) -> PersistenceUserDto | None:
        return self.users.get(str(user_id))

    async def get_user_by_email(self, email: str) -> PersistenceUserDto | None:
        user = next((u for u in self.users.values() if u.email == email), None)
        return user

    async def get_all_users(self) -> list[PersistenceUserDto]:
        return list(self.users.values())
