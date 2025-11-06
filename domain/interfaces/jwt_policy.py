from abc import ABC, abstractmethod

from domain.value_objects.identifiers import UUIDVo


class JwtPolicy(ABC):
    """Interface for domain-level jwt policies."""

    @abstractmethod
    def enforce(self, jti: UUIDVo, revoked_tokens: set[str]) -> None: ...
