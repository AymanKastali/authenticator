from domain.exceptions.error_codes import DomainErrorCodeEnum
from shared.utils.error_data import ErrorData, ErrorDetails


class DomainError(Exception):
    """
    Base class for domain-level errors.
    Handles:
      - code
      - message
      - optional extra metadata
    """

    code: DomainErrorCodeEnum = DomainErrorCodeEnum.GENERAL

    def __init__(self, message: str | None = None, **extra):
        self.message = message or "A domain error occurred."
        self._extra = extra or {}
        super().__init__(self.message)

    def to_dict(self) -> dict:
        details_extra = dict(self._extra)
        error_data = ErrorData(
            error=self.__class__.__name__,
            details=ErrorDetails(
                code=self.code,
                message=self.message,
                extra=details_extra if details_extra else None,
            ),
        )
        return error_data.to_dict()


class InvalidValueError(DomainError):
    code = DomainErrorCodeEnum.INVALID_VALUE

    def __init__(self, field_name: str, message: str | None = None, **extra):
        if message is None:
            message = f"Invalid value for field '{field_name}'."
        super().__init__(message, field=field_name, **extra)


class RequiredFieldError(DomainError):
    code = DomainErrorCodeEnum.REQUIRED_FIELD

    def __init__(self, field_name: str, message: str | None = None, **extra):
        if message is None:
            message = f"The field '{field_name}' is required."
        super().__init__(message, field=field_name, **extra)


class MaxLengthExceededError(DomainError):
    code = DomainErrorCodeEnum.MAX_LENGTH_EXCEEDED

    def __init__(
        self,
        field_name: str,
        max_length: int | None = None,
        message: str | None = None,
        **extra,
    ):
        if message is None:
            if max_length is not None:
                message = (
                    f"'{field_name}' exceeds maximum length of {max_length}."
                )
            else:
                message = f"'{field_name}' has an invalid value."
        super().__init__(
            message, field=field_name, max_length=max_length, **extra
        )


class DomainRuleViolationError(DomainError):
    code = DomainErrorCodeEnum.RULE_VIOLATION

    def __init__(self, message: str, rule_name: str | None = None, **extra):
        super().__init__(message, rule=rule_name, **extra)


class PasswordError(DomainError):
    """
    Represents errors related to password rules or validation.
    """

    code = DomainErrorCodeEnum.PASSWORD_ERROR

    def __init__(
        self, field_name: str = "password", message: str | None = None, **extra
    ):
        """
        Args:
            field_name: Name of the password field (default: "password")
            message: Optional custom message
            **extra: Optional metadata (e.g., min_length, requirements)
        """
        if message is None:
            message = f"Invalid value for '{field_name}'."
        super().__init__(message, field=field_name, **extra)
