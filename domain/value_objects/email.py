import re
from dataclasses import dataclass
from typing import ClassVar

from domain.exceptions.domain_exceptions import InvalidValueError


@dataclass(frozen=True)
class Email:
    value: str

    # ----- Regex pattern as a class constant -----
    EMAIL_PATTERN: ClassVar[str] = (
        r"^[a-zA-Z0-9._%+-]+"  # Local part (username)
        r"@"  # At sign
        r"(?:[a-zA-Z0-9-]+"  # Domain part (non-capturing group)
        r"\.)+"  # Must be followed by a dot (e.g., domain.)
        r"[a-zA-Z]{2,63}$"  # TLD (2 to 63 letters) and end of string
    )

    def __post_init__(self):
        self._validate(self.value)

    # ----- Validation -----
    @classmethod
    def _validate(cls, email: str) -> None:
        if not isinstance(email, str):
            raise InvalidValueError(
                field_name="email", message="Email must be a string."
            )
        if not re.fullmatch(cls.EMAIL_PATTERN, email):
            raise InvalidValueError(
                field_name="email", message="Invalid email format."
            )

    @classmethod
    def from_string(cls, email_str: str) -> "Email":
        """
        Validate the string and return an Email object.
        """
        cls._validate(email_str)
        return cls(value=email_str)
