from domain.enums.error_code_enums import DomainErrorCodeEnum


class DomainError(Exception):
    """Base class for general domain/business logic errors."""

    code: int = DomainErrorCodeEnum.DOMAIN
    status_code: int = 400

    def __init__(self, message: str | None = None):
        self.message = message or "An unexpected domain error occurred."
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Return dict suitable for ErrorResponseModel / JSONResponse."""
        return {
            "status_code": self.status_code,
            "error": self.__class__.__name__,
            "details": {
                "code": self.code,
                "message": self.message,
            },
        }


class InvalidValueError(DomainError):
    code = DomainErrorCodeEnum.INVALID_VALUE
    status_code = 400

    def __init__(
        self,
        field_name: str,
        message: str | None = None,
        invalid_value: object | None = None,
        expected: str | None = None,
    ):
        if message is None:
            parts = [f"Invalid value for '{field_name}'."]
            if invalid_value is not None:
                parts.append(f"Got: {repr(invalid_value)}.")
            if expected is not None:
                parts.append(f"Expected: {expected}.")
            message = " ".join(parts)

        self.field_name = field_name
        super().__init__(message)

    def to_dict(self) -> dict:
        base = super().to_dict()
        base["details"]["field"] = str(self.field_name)
        return base


class InvalidTypeError(DomainError):
    code = DomainErrorCodeEnum.INVALID_TYPE
    status_code = 400

    def __init__(
        self,
        field_name: str,
        expected_type: type | tuple[type, ...],
        actual_value: object,
    ):
        expected_type_names = (
            ", ".join([t.__name__ for t in expected_type])
            if isinstance(expected_type, tuple)
            else expected_type.__name__
        )
        message = (
            f"Invalid type for '{field_name}': expected {expected_type_names}, "
            f"got {type(actual_value).__name__}."
        )
        self.field_name = field_name
        super().__init__(message)

    def to_dict(self) -> dict:
        base = super().to_dict()
        base["details"]["field"] = str(self.field_name)
        return base


class RequiredFieldError(DomainError):
    code = DomainErrorCodeEnum.REQUIRED
    status_code = 400

    def __init__(self, field_name: str, message: str | None = None):
        message = (
            message
            or f"The field '{field_name}' is required but was not provided."
        )
        self.field_name = field_name
        super().__init__(message)

    def to_dict(self) -> dict:
        base = super().to_dict()
        base["details"]["field"] = str(self.field_name)
        return base


class MaxLengthExceededError(DomainError):
    code = DomainErrorCodeEnum.MAX_LENGTH_EXCEEDED
    status_code = 400

    def __init__(
        self,
        field_name: str,
        message: str | None = None,
        max_length: int | None = None,
    ):
        if message is None:
            if max_length is not None:
                message = f"'{field_name}' exceeds the maximum allowed length of {max_length} characters."
            else:
                message = (
                    f"'{field_name}' contains an invalid or unsupported value."
                )
        self.field_name = field_name
        super().__init__(message)

    def to_dict(self) -> dict:
        base = super().to_dict()
        base["details"]["field"] = str(self.field_name)
        return base


class PasswordError(DomainError):
    code = DomainErrorCodeEnum.PASSWORD_ERROR
    status_code = 400

    def __init__(
        self,
        field_name: str,
        message: str | None = None,
    ):
        if message is None:
            parts = [f"Invalid value for '{field_name}'."]
            message = " ".join(parts)

        self.field_name = field_name
        super().__init__(message)

    def to_dict(self) -> dict:
        base = super().to_dict()
        base["details"]["field"] = str(self.field_name)
        return base
