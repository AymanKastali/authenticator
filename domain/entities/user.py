from dataclasses import dataclass, field
from datetime import datetime

from domain.utils.time import make_aware, utc_now
from domain.value_objects.email import Email
from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.identifiers import UUIDId
from domain.value_objects.role import Role


@dataclass(kw_only=True)
class UserEntity:
    uid: UUIDId = field(default_factory=UUIDId.new)
    email: Email
    hashed_password: HashedPassword | None = None
    active: bool = True
    verified: bool = False
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    deleted_at: datetime | None = None
    roles: list[Role] = field(default_factory=lambda: [Role.USER])

    def __post_init__(self):
        self._validate_datetimes()
        self._validate_email()
        self._validate_hashed_password()
        self._validate_roles()
        self._validate_logic()

    # --- mini validation methods ---
    def _validate_datetimes(self):
        object.__setattr__(self, "created_at", make_aware(self.created_at))
        object.__setattr__(self, "updated_at", make_aware(self.updated_at))
        if self.deleted_at is not None:
            object.__setattr__(self, "deleted_at", make_aware(self.deleted_at))

        if self.created_at > utc_now():
            raise ValueError("created_at cannot be in the future")
        if self.updated_at > utc_now():
            raise ValueError("updated_at cannot be in the future")

    def _validate_email(self):
        if not isinstance(self.email, Email):
            raise ValueError("Invalid email value object")

    def _validate_hashed_password(self):
        if self.hashed_password is not None and not isinstance(
            self.hashed_password, HashedPassword
        ):
            raise ValueError("hashed_password must be a HashedPassword VO")

    def _validate_roles(self):
        if not self.roles or not all(isinstance(r, Role) for r in self.roles):
            raise ValueError("User must have at least one valid role")

    def _validate_logic(self):
        if not self.active and self.verified:
            raise ValueError("Inactive users cannot be verified")

    # ----- Factory Methods -----
    def authenticate(self, raw_password: str) -> bool:
        if not self.active:
            raise ValueError("User account is inactive")
        if not self.hashed_password or not self.hashed_password.verify(
            raw_password
        ):
            raise ValueError("Invalid credentials")
        return True

    @staticmethod
    def register_local(
        email: Email, hashed_password: HashedPassword
    ) -> "UserEntity":
        return UserEntity(
            email=email,
            hashed_password=hashed_password,
            active=True,
            verified=False,
        )

    @staticmethod
    def register_external(email: Email) -> "UserEntity":
        return UserEntity(
            email=email, hashed_password=None, active=True, verified=True
        )

    # ----- Business Methods -----
    def verify_password(self, raw_password: str) -> bool:
        if not self.hashed_password:
            return False
        return self.hashed_password.verify(raw_password)

    def change_password(self, new_hashed_password: HashedPassword) -> None:
        object.__setattr__(self, "hashed_password", new_hashed_password)
        object.__setattr__(self, "updated_at", utc_now())

    def deactivate(self) -> None:
        object.__setattr__(self, "active", False)
        object.__setattr__(self, "updated_at", utc_now())

    def activate(self) -> None:
        object.__setattr__(self, "active", True)
        object.__setattr__(self, "updated_at", utc_now())

    def mark_verified(self) -> None:
        object.__setattr__(self, "verified", True)
        object.__setattr__(self, "updated_at", utc_now())
