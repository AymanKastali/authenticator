from datetime import datetime, timedelta, timezone

from application.ports.session_repository import SessionRepositoryPort
from domain.entities.session import Session
from domain.value_objects.uids import SessionId, UUIDId


class InMemorySessionRepository(SessionRepositoryPort):
    """
    In-memory implementation of SessionService.
    Stores sessions in a dictionary with expiry and revocation support.
    """

    def __init__(self, default_ttl: int = 60 * 60 * 24 * 14):
        """
        Args:
            default_ttl: default expiry in seconds (14 days)
        """
        self.sessions: dict[str, Session] = {}
        self.default_ttl = default_ttl

    def create_session(
        self,
        user_id: UUIDId,
        data: dict | None = None,
        expires_seconds: int | None = None,
    ) -> Session:
        now = datetime.now(tz=timezone.utc)
        ttl = expires_seconds or self.default_ttl

        session = Session(
            user_id=user_id,
            created_at=now,
            expires_at=now + timedelta(seconds=ttl),
            data=data or {},
            is_active=True,
            last_activity=now,
        )

        self.sessions[session.uid.value] = session
        return session

    def get_session(self, session_id: SessionId) -> Session | None:
        session = self.sessions.get(session_id.value)
        now = datetime.now(tz=timezone.utc)
        if not session:
            return None
        if not session.is_active or session.expires_at < now:
            return None
        return session

    def revoke_session(self, session_id: SessionId) -> None:
        session = self.sessions.get(session_id.value)
        if session:
            session.is_active = False
            session.revoked_at = datetime.now(tz=timezone.utc)

    def refresh_session(self, session_id: SessionId) -> Session | None:
        session = self.get_session(session_id)
        if not session:
            return None
        now = datetime.now(tz=timezone.utc)
        session.last_activity = now
        # extend expiry by default TTL
        session.expires_at = now + timedelta(seconds=self.default_ttl)
        return session
