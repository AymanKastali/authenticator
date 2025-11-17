from dataclasses import dataclass, field

from domain.exceptions.domain_errors import (
    DomainRuleViolationError,
    UserDeletedError,
    UserInactiveError,
)
from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.email import EmailVo
from domain.value_objects.hashed_password import HashedPasswordVo
from domain.value_objects.role import RoleVo
from domain.value_objects.user_status import UserStatusVo
from domain.value_objects.uuid_id import UUIDVo


@dataclass(slots=True, kw_only=True)
class UserEntity:
    """Domain entity representing a User. No validation here — factory handles it."""

    uid: UUIDVo
    _email: EmailVo = field(repr=False)
    _hashed_password: HashedPasswordVo | None = field(repr=False)
    _status: UserStatusVo
    created_at: DateTimeVo
    deleted_at: DateTimeVo | None
    roles: list[RoleVo]

    # ----- Properties -----
    @property
    def email(self) -> EmailVo:
        return self._email

    @property
    def hashed_password(self) -> HashedPasswordVo | None:
        return self._hashed_password

    @property
    def status(self) -> UserStatusVo:
        return self._status

    @property
    def is_active(self) -> bool:
        return self._status in {UserStatusVo.ACTIVE, UserStatusVo.VERIFIED}

    @property
    def is_verified(self) -> bool:
        return self._status == UserStatusVo.VERIFIED

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    # ----- Actions -----
    def activate(self):
        self._change_status(UserStatusVo.ACTIVE)

    def deactivate(self):
        self._change_status(UserStatusVo.INACTIVE)

    def mark_verified(self):
        self._change_status(UserStatusVo.VERIFIED)

    def change_password(self, new_hashed_password: HashedPasswordVo):
        self._hashed_password = new_hashed_password

    # ----- Internal -----
    def _change_status(self, new_status: UserStatusVo):
        if self._status == new_status:
            raise DomainRuleViolationError(
                message=f"User already in status: {new_status.value}",
                rule_name="UserStatusTransitionRule",
            )
        self._status = new_status

    # ----- Validations -----
    def ensure_active(self):
        if self.is_active is False:
            raise UserInactiveError(self.uid.value)

    def ensure_not_deleted(self):
        if self.is_deleted is True:
            raise UserDeletedError(self.uid.value)
