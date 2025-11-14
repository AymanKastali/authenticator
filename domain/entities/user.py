from dataclasses import dataclass, field
from typing import Self

from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.email import EmailVo
from domain.value_objects.hashed_password import HashedPasswordVo
from domain.value_objects.identifiers import UUIDVo
from domain.value_objects.role import RoleVo
from domain.value_objects.user_status import UserStatusVo


@dataclass(slots=True, kw_only=True)
class UserEntity:
    uid: UUIDVo
    _email: EmailVo = field(repr=False)
    _hashed_password: HashedPasswordVo | None = field(default=None, repr=False)
    _status: UserStatusVo = field(default=UserStatusVo.PENDING_VERIFICATION)
    created_at: DateTimeVo = field(default_factory=DateTimeVo.now)
    updated_at: DateTimeVo = field(default_factory=DateTimeVo.now)
    deleted_at: DateTimeVo | None = None
    roles: list[RoleVo] = field(default_factory=lambda: [RoleVo.USER])

    def __post_init__(self):
        self.validate()

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
    def active(self) -> bool:
        return self._status in {UserStatusVo.ACTIVE, UserStatusVo.VERIFIED}

    @property
    def verified(self) -> bool:
        return self._status == UserStatusVo.VERIFIED

    @property
    def deleted(self) -> bool:
        return self.deleted_at is not None

    # ----------------- Status Transitions -----------------
    def activate(self):
        self._set_status(UserStatusVo.ACTIVE)

    def deactivate(self):
        self._set_status(UserStatusVo.INACTIVE)

    def mark_verified(self):
        self._set_status(UserStatusVo.VERIFIED)

    def _set_status(self, new_status: UserStatusVo):
        if self._status == new_status:
            raise ValueError(f"User is already {new_status.value}")
        self._status = new_status
        self._touch()

    # ----------------- Password -----------------
    def change_password(self, new_hashed_password: HashedPasswordVo):
        self._hashed_password = new_hashed_password
        self._touch()

    # ----------------- Internal -----------------
    def _touch(self):
        self.updated_at = DateTimeVo.now()

    # ----------------- Validation -----------------
    def validate(self):
        if self.created_at.is_future():
            raise ValueError("created_at cannot be in the future")
        if self.updated_at.is_future():
            raise ValueError("updated_at cannot be in the future")
        if self.deleted_at is not None and self.deleted_at.is_future():
            raise ValueError("deleted_at cannot be in the future")
        if not self.roles or not all(isinstance(r, RoleVo) for r in self.roles):
            raise ValueError("User must have at least one valid role")
        if not self.active and self.verified:
            raise ValueError("Inactive users cannot be verified")

    # ----------------- Factory Methods -----------------
    @classmethod
    def create_local(
        cls,
        email: EmailVo,
        hashed_password: HashedPasswordVo,
        roles: list[RoleVo] | None = None,
    ) -> Self:
        """Create a local user pending verification"""
        uid = UUIDVo.new()
        return cls(
            uid=uid,
            _email=email,
            _hashed_password=hashed_password,
            _status=UserStatusVo.PENDING_VERIFICATION,
            roles=roles or [RoleVo.USER],
        )

    @classmethod
    def create_external(
        cls, email: EmailVo, roles: list[RoleVo] | None = None
    ) -> Self:
        """Create an external (OAuth) verified user"""
        uid = UUIDVo.new()
        return cls(
            uid=uid,
            _email=email,
            _hashed_password=None,
            _status=UserStatusVo.VERIFIED,
            roles=roles or [RoleVo.USER],
        )
