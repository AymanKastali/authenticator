from abc import ABC, abstractmethod

from domain.value_objects.policy_description import PolicyDescriptionVo


class PasswordPolicyInterface(ABC):
    """Interface for domain-level password policies."""

    @abstractmethod
    def enforce(self, password: str) -> None: ...

    @abstractmethod
    def describe(self) -> PolicyDescriptionVo: ...
