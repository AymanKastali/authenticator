from abc import ABC, abstractmethod

from domain.entities.user import User
from domain.value_objects.email import EmailAddress
from domain.value_objects.uids import UUIDId


class UserRepositoryPort(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: UUIDId) -> User | None: ...

    @abstractmethod
    def find_by_email(self, email: EmailAddress) -> User | None: ...

    @abstractmethod
    def save(self, user: User) -> None: ...

    @abstractmethod
    def get_all_users(self) -> list[User]: ...
