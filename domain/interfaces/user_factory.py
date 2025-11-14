from abc import ABC, abstractmethod

from domain.entities.user import UserEntity
from domain.value_objects.email import EmailVo
from domain.value_objects.hashed_password import HashedPasswordVo
from domain.value_objects.role import RoleVo


class UserFactoryInterface(ABC):
    """Abstract factory interface for creating UserEntity instances."""

    @abstractmethod
    def create_local_user(
        self,
        email: EmailVo,
        hashed_password: HashedPasswordVo,
        roles: list[RoleVo] | None = None,
    ) -> UserEntity: ...

    @abstractmethod
    def create_external_user(
        self,
        email: EmailVo,
        roles: list[RoleVo] | None = None,
    ) -> UserEntity: ...
