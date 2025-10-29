from abc import ABC, abstractmethod


class PasswordPolicy(ABC):
    """Interface for domain-level password policies."""

    @abstractmethod
    def enforce(self, password: str) -> None: ...
