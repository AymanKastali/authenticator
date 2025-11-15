from dataclasses import dataclass, field

from domain.exceptions.domain_errors import (
    DomainRuleViolationError,
    InvalidValueError,
)
from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.email import EmailVo
from domain.value_objects.hashed_password import HashedPasswordVo
from domain.value_objects.role import RoleVo
from domain.value_objects.user_status import UserStatusVo
from domain.value_objects.uuid_id import UUIDVo


@dataclass(slots=True, kw_only=True)
class UserEntity:
    """A domain entity representing a User with strong invariants and explicit construction."""

    uid: UUIDVo
    _email: EmailVo = field(repr=False)
    _hashed_password: HashedPasswordVo | None = field(repr=False)
    _status: UserStatusVo
    created_at: DateTimeVo
    updated_at: DateTimeVo
    deleted_at: DateTimeVo | None
    roles: list[RoleVo]

    def __post_init__(self):
        self._validate()

    # ----------------- Properties -----------------
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

    # ----------------- Status Transitions -----------------
    def activate(self):
        self._change_status(UserStatusVo.ACTIVE)

    def deactivate(self):
        self._change_status(UserStatusVo.INACTIVE)

    def mark_verified(self):
        self._change_status(UserStatusVo.VERIFIED)

    def _change_status(self, new_status: UserStatusVo):
        if self._status == new_status:
            raise DomainRuleViolationError(
                message=f"User is already in status: {new_status.value}",
                rule_name="UserStatusTransitionRule",
            )
        self._status = new_status
        self._touch()

    # ----------------- Password -----------------
    def change_password(self, new_hashed_password: HashedPasswordVo):
        self._hashed_password = new_hashed_password
        self._touch()

    # ----------------- Internal -----------------
    def _touch(self):
        self.updated_at = DateTimeVo.now()

    # ----------------- Validation (Atomic) -----------------
    def _validate(self):
        self._validate_dates()
        self._validate_roles()
        self._validate_status_invariants()

    def _validate_dates(self):
        if self.created_at.is_future():
            raise InvalidValueError(
                field_name="created_at",
                message="created_at cannot be in the future",
            )
        if self.updated_at.is_future():
            raise InvalidValueError(
                field_name="updated_at",
                message="updated_at cannot be in the future",
            )

        if self.deleted_at and self.deleted_at.is_future():
            raise InvalidValueError(
                field_name="deleted_at",
                message="deleted_at cannot be in the future",
            )

    def _validate_roles(self):
        if not self.roles or not all(isinstance(r, RoleVo) for r in self.roles):
            raise InvalidValueError(
                field_name="roles",
                message="User must have at least one valid role",
            )

    def _validate_status_invariants(self):
        if not self.is_active and self.is_verified:
            raise DomainRuleViolationError(
                message="Inactive users cannot be verified",
                rule_name="UserStatusRule",
            )
