from abc import ABC, abstractmethod

from domain.value_objects.identifiers import UUIDId


class JwtPolicy(ABC):
    """Interface for domain-level jwt policies."""

    @abstractmethod
    def enforce(self, jti: UUIDId, revoked_tokens: set[str]) -> None: ...
