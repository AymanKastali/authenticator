from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class Token:
    value: str
    expires_at: datetime

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at
