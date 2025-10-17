from abc import ABC, abstractmethod

from domain.entities.user import User
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.user_id import UserId


class IUserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: UserId) -> User | None:
        pass

    @abstractmethod
    def find_by_email(self, email: EmailAddress) -> User | None:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass
