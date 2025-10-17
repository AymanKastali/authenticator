from domain.entities.user import User
from domain.interfaces.user import IUserRepository
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.user_id import UserId


class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users: dict[str, User] = {}

    def find_by_id(self, user_id: UserId) -> User | None:
        return self.users.get(user_id.value)

    def find_by_email(self, email: EmailAddress) -> User | None:
        return next(
            (u for u in self.users.values() if u.email.value == email.value),
            None,
        )

    def save(self, user: User) -> None:
        self.users[user.id.value] = user
