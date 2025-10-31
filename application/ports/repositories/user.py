from abc import ABC, abstractmethod
from uuid import UUID

from application.dto.user.persistence import PersistenceUserDto


class UserRepositoryPort(ABC):
    @abstractmethod
    def save(self, user: PersistenceUserDto) -> None: ...

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> PersistenceUserDto | None: ...

    @abstractmethod
    def get_user_by_email(self, email: str) -> PersistenceUserDto | None: ...

    @abstractmethod
    def get_all_users(self) -> list[PersistenceUserDto]: ...
