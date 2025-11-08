from abc import ABC, abstractmethod
from typing import Self

from domain.interfaces.policy import PolicyInterface


class PolicyBuilderInterface(ABC):
    """Assemble domain policies from config or custom overrides."""

    @abstractmethod
    def add_policy(self, policy: PolicyInterface) -> Self: ...

    @abstractmethod
    def build(self) -> list[PolicyInterface]: ...
