from application.ports.user_repository import UserRepositoryPort
from domain.entities.user import User
from domain.value_objects.email import EmailAddress
from domain.value_objects.uids import UUIDId


class InMemoryUserRepository(UserRepositoryPort):
    def __init__(self):
        self.users: dict[str, User] = {}

    def get_user_by_id(self, user_id: UUIDId) -> User | None:
        return self.users.get(str(user_id.value))

    def find_by_email(self, email: EmailAddress) -> User | None:
        return next(
            (u for u in self.users.values() if u.email.value == email.value),
            None,
        )

    def save(self, user: User) -> None:
        self.users[str(user.uid.value)] = user

    def get_all_users(self) -> list[User]:
        return list(self.users.values())
