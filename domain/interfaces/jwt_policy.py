from abc import ABC, abstractmethod

from domain.value_objects.identifiers import UUIDIdVo


class JwtPolicy(ABC):
    """Interface for domain-level jwt policies."""

    @abstractmethod
    def enforce(self, jti: UUIDIdVo, revoked_tokens: set[str]) -> None: ...
