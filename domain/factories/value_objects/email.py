import re

from domain.exceptions.domain_errors import InvalidValueError
from domain.value_objects.email import EmailVo


class EmailVoFactory:
    """Responsible for creating valid EmailVo instances."""

    EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,63})+$"

    @classmethod
    def create(cls, email_str: str) -> EmailVo:
        normalized = cls._enforce_normalized(email_str)
        cls._enforce_type(normalized)
        cls._enforce_format(normalized)
        return EmailVo(_value=normalized)

    @classmethod
    def from_string(cls, value: str) -> EmailVo:
        """Reconstruct a VO from a string assumed to be already validated."""
        normalized = cls._enforce_normalized(value)
        return EmailVo(_value=normalized)

    # ----------------- Mini Enforcement Methods -----------------
    @classmethod
    def _enforce_normalized(cls, value: str) -> str:
        return value.strip().lower()

    @classmethod
    def _enforce_type(cls, value: str) -> None:
        if not isinstance(value, str):
            raise InvalidValueError(
                field_name="email", message="Email must be a string."
            )

    @classmethod
    def _enforce_format(cls, value: str) -> None:
        if not re.fullmatch(cls.EMAIL_PATTERN, value):
            raise InvalidValueError(
                field_name="email", message="Invalid email format."
            )
