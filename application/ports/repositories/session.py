from abc import ABC, abstractmethod

from application.dto.auth.session.persistence import PersistenceSessionDto


class SessionRepositoryPort(ABC):
    @abstractmethod
    def create_session(
        self, session: PersistenceSessionDto
    ) -> PersistenceSessionDto: ...
