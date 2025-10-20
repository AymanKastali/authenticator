from abc import ABC, abstractmethod

from domain.entities.user import User
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.uids import UUIDId


class UserRepositoryPort(ABC):
    @abstractmethod
    def find_by_id(self, user_id: UUIDId) -> User | None: ...

    @abstractmethod
    def find_by_email(self, email_address: EmailAddress) -> User | None: ...

    @abstractmethod
    def save(self, user: User) -> None: ...
