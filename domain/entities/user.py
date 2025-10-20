from dataclasses import dataclass, field
from datetime import datetime

from domain.utils.date_time import utc_now
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.uids import UUIDId


@dataclass(kw_only=True)
class User:
    uid: UUIDId = field(default_factory=UUIDId.new)
    email_address: EmailAddress
    hashed_password: HashedPassword | None = None
    is_active: bool = True
    active: bool = True
    verified: bool = False
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    deleted_at: datetime | None = None

    # ----- Factory Methods -----
    @staticmethod
    def register_local(email_address: EmailAddress, password: str) -> "User":
        """Register a user with email_address and password (local credentials)."""
        return User(
            email_address=email_address,
            hashed_password=HashedPassword.from_plain(password),
            active=True,
            verified=False,
        )

    @staticmethod
    def register_external(email_address: EmailAddress) -> "User":
        """Register a user authenticated via OAuth/SSO."""
        return User(
            email_address=email_address,
            hashed_password=None,
            active=True,
            verified=True,  # usually verified by external provider
        )

    # ----- Business Methods -----
    def verify_password(self, password: str) -> bool:
        if not self.hashed_password:
            return False
        return self.hashed_password.verify(password)

    def change_password(self, new_password: str):
        self.hashed_password = HashedPassword.from_plain(new_password)
        self.updated_at = utc_now()

    def deactivate(self):
        self.active = False
        self.updated_at = utc_now()

    def activate(self):
        self.active = True
        self.updated_at = utc_now()

    def mark_verified(self):
        self.verified = True
        self.updated_at = utc_now()
