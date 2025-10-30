from datetime import datetime, timezone

from application.ports.repositories.jwt import JwtRepositoryPort


class InMemoryJwtRepository(JwtRepositoryPort):
    def __init__(self):
        self._tokens: dict[str, datetime] = {}

    def add_token(self, jti: str, expires_at: datetime) -> None:
        self._tokens[jti] = expires_at

    def get_revoked_tokens(self) -> set[str]:
        now = datetime.now(timezone.utc)
        # cleanup expired tokens
        self._tokens = {
            jti: exp for jti, exp in self._tokens.items() if exp > now
        }
        return set(self._tokens.keys())
