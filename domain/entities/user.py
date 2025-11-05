from dataclasses import dataclass, field

from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.email import EmailVo
from domain.value_objects.hashed_password import HashedPasswordVo
from domain.value_objects.identifiers import UUIDIdVo
from domain.value_objects.role import RoleVo
from domain.value_objects.user_status import UserStatusVo


@dataclass(slots=True, kw_only=True)
class UserEntity:
    uid: UUIDIdVo = field(default_factory=UUIDIdVo.new)
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

    @email.setter
    def email(self, value: EmailVo):
        if not isinstance(value, EmailVo):
            raise ValueError("Invalid email value object")
        self._email = value
        self._touch()

    @property
    def hashed_password(self) -> HashedPasswordVo | None:
        return self._hashed_password

    @hashed_password.setter
    def hashed_password(self, value: HashedPasswordVo):
        if value is not None and not isinstance(value, HashedPasswordVo):
            raise ValueError("hashed_password must be a HashedPasswordVo VO")
        self._hashed_password = value
        self._touch()

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

    # Status changes must go through methods
    def _set_status(self, new_status: UserStatusVo):
        if self._status == new_status:
            raise ValueError(f"User is already {new_status.value}")
        self._status = new_status
        self._touch()

    # ----------------- Internal Methods -----------------
    def _touch(self):
        self.updated_at = DateTimeVo.now()

    # ----------------- Validation -----------------
    def ensure_valid_created_at(self):
        if self.created_at.is_future():
            raise ValueError("created_at cannot be in the future")

    def ensure_valid_updated_at(self):
        if self.updated_at.is_future():
            raise ValueError("updated_at cannot be in the future")

    def ensure_valid_deleted_at(self):
        if self.deleted_at is not None and self.deleted_at.is_future():
            raise ValueError("deleted_at cannot be in the future")

    def ensure_valid_roles(self):
        if not self.roles or not all(isinstance(r, RoleVo) for r in self.roles):
            raise ValueError("User must have at least one valid role")

    def ensure_valid_logic(self):
        if not self.active and self.verified:
            raise ValueError("Inactive users cannot be verified")

    def validate(self):
        self.ensure_valid_created_at()
        self.ensure_valid_updated_at()
        self.ensure_valid_deleted_at()
        self.ensure_valid_roles()
        self.ensure_valid_logic()

    # ----------------- Factory Methods -----------------
    @staticmethod
    def create(
        email: EmailVo,
        hashed_password: HashedPasswordVo | None = None,
        roles: list[RoleVo] | None = None,
    ) -> "UserEntity":
        """Create a new user (local or external)"""
        return UserEntity(
            _email=email,
            _hashed_password=hashed_password,
            _status=UserStatusVo.VERIFIED
            if hashed_password is None
            else UserStatusVo.PENDING_VERIFICATION,
            roles=roles or [RoleVo.USER],
        )

    # ----------------- Business Methods -----------------
    def authenticate(self, raw_password: str) -> bool:
        if not self.active:
            raise ValueError("User account is inactive")
        if not self.hashed_password or not self.hashed_password.verify(
            raw_password
        ):
            raise ValueError("Invalid credentials")
        return True

    def verify_password(self, raw_password: str) -> bool:
        if not self.hashed_password:
            return False
        return self.hashed_password.verify(raw_password)

    def change_password(self, new_hashed_password: HashedPasswordVo):
        self.hashed_password = new_hashed_password

    def deactivate(self):
        self._set_status(UserStatusVo.INACTIVE)

    def activate(self):
        self._set_status(UserStatusVo.ACTIVE)

    def mark_verified(self):
        self._set_status(UserStatusVo.VERIFIED)
