from abc import ABC, abstractmethod

from domain.value_objects.policy_description import PolicyDescriptionVo


class JwtPolicyInterface(ABC):
    """Interface for domain-level jwt policies."""

    @abstractmethod
    def enforce(self, token: str) -> None: ...

    @abstractmethod
    def describe(self) -> PolicyDescriptionVo: ...
