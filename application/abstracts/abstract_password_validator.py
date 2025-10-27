from abc import ABC, abstractmethod

from domain.exceptions.domain_errors import PasswordError


class AbstractPasswordValidator(ABC):
    """Abstract interface for password validation."""

    @abstractmethod
    def validate(self, password: str) -> None:
        pass

    def _raise(self, message: str, field_name: str = "password") -> None:
        raise PasswordError(
            message=message,
            field_name=field_name,
        )
