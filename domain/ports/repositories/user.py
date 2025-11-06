from abc import ABC, abstractmethod

from domain.entities.user import UserEntity
from domain.value_objects.email import EmailVo
from domain.value_objects.identifiers import UUIDVo


class UserRepositoryPort(ABC):
    @abstractmethod
    async def save(self, user: UserEntity) -> None: ...

    @abstractmethod
    async def get_user_by_id(self, user_id: UUIDVo) -> UserEntity | None: ...

    @abstractmethod
    async def get_user_by_email(self, email: EmailVo) -> UserEntity | None: ...

    @abstractmethod
    async def get_all_users(self) -> list[UserEntity]: ...
