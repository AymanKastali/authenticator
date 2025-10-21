from domain.value_objects.email import EmailAddress

from application.ports.user_repository import UserRepositoryPort
from domain.entities.user import User
from domain.value_objects.uids import UUIDId


class InMemoryUserRepository(UserRepositoryPort):
    def __init__(self):
        self.users: dict[str, User] = {}

    def find_by_id(self, user_id: UUIDId) -> User | None:
        return self.users.get(user_id.value)

    def find_by_email(self, email: EmailAddress) -> User | None:
        return next(
            (u for u in self.users.values() if u.email.value == email.value),
            None,
        )

    def save(self, user: User) -> None:
        self.users[user.uid.value] = user
