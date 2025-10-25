from dataclasses import dataclass, field
from datetime import datetime

from domain.config.config_models import PasswordConfig
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
    def register_local(
        email: Email, password: str, password_cfg: PasswordConfig
    ) -> "User":
        """Register a user with email and password (local credentials)."""
        return User(
            email=email,
            hashed_password=HashedPassword.from_plain(password, password_cfg),
            active=True,
            verified=False,
        )

    @staticmethod
    def register_external(email: Email) -> "User":
        """Register a user authenticated via OAuth/SSO."""
        return User(
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

    def change_password(self, new_password: str, password_cfg: PasswordConfig):
        self.hashed_password = HashedPassword.from_plain(
            new_password, password_cfg
        )
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
