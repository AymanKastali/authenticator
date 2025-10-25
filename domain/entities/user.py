from dataclasses import dataclass, field
from datetime import datetime

from domain.utils.date_time_utils import utc_now
from domain.value_objects.email import Email
from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.identifiers import UUIDId
from domain.value_objects.role import Role


@dataclass(kw_only=True)
class User:
    uid: UUIDId = field(default_factory=UUIDId.new)
    email: Email
    hashed_password: HashedPassword | None = None
    active: bool = True
    verified: bool = False
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    deleted_at: datetime | None = None
    roles: list[Role] = field(default_factory=lambda: [Role.USER])

    # ----- Factory Methods -----
    @staticmethod
    def register_local(email: Email, hashed_password: HashedPassword) -> "User":
        """Register a user with local credentials."""
        return User(
            email=email,
            hashed_password=hashed_password,
            active=True,
            verified=False,
        )

    @staticmethod
    def register_external(email: Email) -> "User":
        """Register a user authenticated via an external provider."""
        return User(
            email=email,
            hashed_password=None,
            active=True,
            verified=True,
        )

    # ----- Business Methods -----
    def verify_password(self, raw_password: str) -> bool:
        """Check if the given raw password matches the stored hash."""
        if not self.hashed_password:
            return False
        return self.hashed_password.verify(raw_password)

    def change_password(self, new_hashed_password: HashedPassword) -> None:
        """Change password with a pre-hashed value."""
        self.hashed_password = new_hashed_password
        self.updated_at = utc_now()

    def deactivate(self) -> None:
        self.active = False
        self.updated_at = utc_now()

    def activate(self) -> None:
        self.active = True
        self.updated_at = utc_now()

    def mark_verified(self) -> None:
        self.verified = True
        self.updated_at = utc_now()
