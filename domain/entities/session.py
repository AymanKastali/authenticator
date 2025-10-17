from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
from domain.value_objects.token import Token

@dataclass
class SessionEntity:
    id: str
    user_id: str
    token: Token
    created_at: datetime = field(default_factory=datetime.now(timezone.utc))
    revoked: bool = False

    @staticmethod
    def create(user_id: str, token: Token) -> "SessionEntity":
        return SessionEntity(id=str(uuid4()), user_id=user_id, token=token)

    def revoke(self):
        self.revoked = True
