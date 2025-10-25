from abc import ABC, abstractmethod

from domain.entities.session import Session
from domain.value_objects.identifiers import UUIDId


class SessionRepositoryPort(ABC):
    @abstractmethod
    def create_session(
        self,
        user_id: UUIDId,
        data: dict | None = None,
        expires_seconds: int | None = None,
    ) -> Session: ...

    @abstractmethod
    def get_session(self, session_id: str) -> Session | None: ...

    @abstractmethod
    def revoke_session(self, session_id: str) -> None: ...

    @abstractmethod
    def refresh_session(self, session_id: str) -> Session | None: ...
