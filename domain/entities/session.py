from dataclasses import dataclass, field
from datetime import datetime, timedelta

from domain.utils.date_time_utils import utc_now
from domain.value_objects.identifiers import SessionId, UUIDId


@dataclass(kw_only=True)
class Session:
    uid: SessionId = field(default_factory=SessionId.new)
    user_id: UUIDId
    created_at: datetime = field(default_factory=utc_now)
    expires_at: datetime
    ip_address: str | None = None
    user_agent: str | None = None
    data: dict = field(default_factory=dict)
    is_active: bool = True
    revoked_at: datetime | None = None
    last_activity: datetime | None = None

    @staticmethod
    def new(
        user_id: UUIDId, duration_seconds: int = 1209600, **metadata
    ) -> "Session":
        return Session(
            user_id=user_id,
            expires_at=utc_now() + timedelta(seconds=duration_seconds),
            **metadata,
        )

    def revoke(self) -> None:
        self.is_active = False
        self.revoked_at = utc_now()

    def refresh(self, duration_seconds: int = 1209600) -> None:
        self.expires_at = utc_now() + timedelta(seconds=duration_seconds)
        self.last_activity = utc_now()
