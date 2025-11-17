from abc import ABC, abstractmethod

from domain.entities.session import SessionEntity


class SessionRepositoryPort(ABC):
    @abstractmethod
    # TODO fix params and return type
    def create(self, session: SessionEntity) -> SessionEntity: ...
