from dataclasses import dataclass, field
from datetime import datetime

from domain.value_objects.session_id import SessionIdVo
from domain.value_objects.uuid_id import UUIDVo


@dataclass(slots=True, kw_only=True)
class SessionEntity:
    uid: SessionIdVo
    user_id: UUIDVo
    created_at: datetime
    expires_at: datetime
    ip_address: str | None = None
    user_agent: str | None = None
    data: dict = field(default_factory=dict)
    is_active: bool = True
    revoked_at: datetime | None = None
    last_activity: datetime | None = None

    # @classmethod
    # def create(
    #     cls, user_id: UUIDVo, duration_seconds: int = 1209600, **metadata
    # ) -> "SessionEntity":
    #     return cls(
    #         user_id=user_id,
    #         expires_at=utc_now() + timedelta(seconds=duration_seconds),
    #         **metadata,
    #     )

    # def revoke(self) -> None:
    #     self.is_active = False
    #     self.revoked_at = utc_now()

    # def refresh(self, duration_seconds: int = 1209600) -> None:
    #     self.expires_at = utc_now() + timedelta(seconds=duration_seconds)
    #     self.last_activity = utc_now()
