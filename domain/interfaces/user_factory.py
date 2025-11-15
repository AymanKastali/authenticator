from __future__ import annotations

from abc import ABC, abstractmethod

from domain.entities.user import UserEntity
from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.email import EmailVo
from domain.value_objects.hashed_password import HashedPasswordVo
from domain.value_objects.role import RoleVo
from domain.value_objects.user_status import UserStatusVo


class UserEntityFactoryInterface(ABC):
    """Interface for a factory responsible for creating UserEntity instances."""

    @classmethod
    @abstractmethod
    def create(
        cls,
        *,
        email: EmailVo,
        status: UserStatusVo,
        hashed_password: HashedPasswordVo | None = None,
        deleted_at: DateTimeVo | None = None,
        roles: list[RoleVo],
    ) -> UserEntity: ...
