from dataclasses import dataclass, field
from datetime import datetime

from domain.utils.time_utils import utc_now
from domain.value_objects.user_id import UserId

from ..value_objects.email_address import EmailAddress
from ..value_objects.hashed_password import HashedPassword


@dataclass
class User:
    id: UserId
    email: EmailAddress
    hashed_password: HashedPassword | None
    is_active: bool = True
    active: bool = True
    verified: bool = False
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    # ----- Factory Methods -----
    @staticmethod
    def register_local(email: EmailAddress, password: str) -> "User":
        """Register a user with email and password (local credentials)."""
        return User(
            id=UserId.new(),
            email=email,
            hashed_password=HashedPassword.from_plain(password),
            active=True,
            verified=False,
        )

    @staticmethod
    def register_external(email: EmailAddress) -> "User":
        """Register a user authenticated via OAuth/SSO."""
        return User(
            id=UserId.new(),
            email=email,
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
