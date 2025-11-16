from application.dto.auth.session.persistence import PersistenceSessionDto
from application.ports.repositories.session import SessionRepositoryPort
from infrastructure.gateways.persistence.in_memory.db.storage import (
    InMemorySessionStorage,
)


class InMemorySessionRepository(SessionRepositoryPort):
    """
    In-memory implementation of SessionService.
    Stores sessions in a dictionary with expiry and revocation support.
    """

    def __init__(self, storage: InMemorySessionStorage):
        self._storage = storage

    def create_session(
        self, session: PersistenceSessionDto
    ) -> PersistenceSessionDto:
        self._storage.sessions[session.session_id] = session
        return session
