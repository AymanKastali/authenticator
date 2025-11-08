from abc import ABC, abstractmethod

from domain.value_objects.policy_description import PolicyDescriptionVo


class PolicyInterface(ABC):
    """Base interface for all domain policies."""

    @abstractmethod
    def enforce(self, target: object) -> None: ...

    @abstractmethod
    def describe(self) -> PolicyDescriptionVo: ...
