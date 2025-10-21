from abc import ABC, abstractmethod

from domain.value_objects.email import EmailAddress

from domain.entities.user import User
from domain.value_objects.uids import UUIDId


class UserRepositoryPort(ABC):
    @abstractmethod
    def find_by_id(self, user_id: UUIDId) -> User | None: ...

    @abstractmethod
    def find_by_email(self, email: EmailAddress) -> User | None: ...

    @abstractmethod
    def save(self, user: User) -> None: ...
