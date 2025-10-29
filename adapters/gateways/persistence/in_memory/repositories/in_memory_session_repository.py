from application.dto.auth.session.persistence import PersistenceSessionDto
from application.ports.repositories.session import SessionRepositoryPort


class InMemorySessionRepository(SessionRepositoryPort):
    """
    In-memory implementation of SessionService.
    Stores sessions in a dictionary with expiry and revocation support.
    """

    def __init__(self):
        self.sessions: dict[str, PersistenceSessionDto] = {}

    def create_session(
        self, session: PersistenceSessionDto
    ) -> PersistenceSessionDto:
        self.sessions[session.session_id] = session
        return session
