from abc import ABC, abstractmethod

from application.dto.session import PersistenceSessionDto


class SessionRepositoryPort(ABC):
    @abstractmethod
    def create_session(
        self, session: PersistenceSessionDto
    ) -> PersistenceSessionDto: ...
