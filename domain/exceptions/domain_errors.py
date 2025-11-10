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


# ------------------------- JWT Related Domain Errors -------------------------
class JwtError(DomainError):
    """Base class for JWT-related domain errors."""

    code = DomainErrorCodeEnum.JWT_ERROR


class JwtExpiredError(JwtError):
    """Token has expired."""

    code = DomainErrorCodeEnum.JWT_EXPIRED

    def __init__(self, message: str | None = None, **extra):
        message = message or "JWT token has expired."
        super().__init__(message, **extra)


class JwtRevokedError(JwtError):
    """Token has been revoked/blacklisted."""

    code = DomainErrorCodeEnum.JWT_REVOKED

    def __init__(self, message: str | None = None, **extra):
        message = message or "JWT token has been revoked."
        super().__init__(message, **extra)


class JwtInvalidError(JwtError):
    """Token is invalid (signature, structure, or claims)."""

    code = DomainErrorCodeEnum.JWT_INVALID

    def __init__(self, message: str | None = None, **extra):
        message = message or "JWT token is invalid."
        super().__init__(message, **extra)


class JwtNotYetValidError(JwtError):
    """Token 'nbf' claim prevents it from being used yet."""

    code = DomainErrorCodeEnum.JWT_NOT_YET_VALID

    def __init__(self, message: str | None = None, **extra):
        message = message or "JWT token is not yet valid (nbf)."
        super().__init__(message, **extra)


# ------------------------- User Related Domain Errors -------------------------
class UserDomainError(DomainError):
    """Base class for all User domain errors."""

    code = DomainErrorCodeEnum.OPERATION_NOT_ALLOWED


class UserAlreadyExistsError(UserDomainError):
    """Raised when trying to create/register a user that already exists."""

    code = DomainErrorCodeEnum.UNIQUE_CONSTRAINT_VIOLATION

    def __init__(self, email: str, message: str | None = None, **extra):
        if message is None:
            message = f"User with email '{email}' already exists."
        super().__init__(message, email=email, **extra)


class UserNotFoundError(UserDomainError):
    """Raised when a user cannot be found by ID or email."""

    code = DomainErrorCodeEnum.NOT_FOUND

    def __init__(self, identifier: str, message: str | None = None, **extra):
        id_value = (
            identifier if hasattr(identifier, "to_string") else str(identifier)
        )
        if message is None:
            message = f"User with identifier '{id_value}' not found."
        super().__init__(message, identifier=id_value, **extra)


class UserInactiveError(UserDomainError):
    """Raised when the user account is inactive."""

    code = DomainErrorCodeEnum.OPERATION_NOT_ALLOWED

    def __init__(self, user_id: str, message: str | None = None, **extra):
        if message is None:
            message = f"User '{user_id}' is inactive."
        super().__init__(message, user_id=user_id, **extra)


class UserDeletedError(UserDomainError):
    """Raised when the user account is deleted."""

    code = DomainErrorCodeEnum.OPERATION_NOT_ALLOWED

    def __init__(self, user_id: str, message: str | None = None, **extra):
        if message is None:
            message = f"User '{user_id}' is deleted."
        super().__init__(message, user_id=user_id, **extra)


class InvalidCredentialsError(UserDomainError):
    """Raised when authentication fails due to invalid password."""

    code = DomainErrorCodeEnum.INVALID_VALUE

    def __init__(self, email: str, message: str | None = None, **extra):
        if message is None:
            message = f"Invalid credentials for '{email}'."
        super().__init__(message, email=email, **extra)


# ------------------------- Password Related Domain Errors -------------------------
class PasswordError(DomainError):
    """Base class for password-related domain errors."""

    code = DomainErrorCodeEnum.PASSWORD_ERROR


class PasswordVerificationError(PasswordError):
    """Raised when password verification fails."""

    def __init__(self, message: str = "Password verification failed.", **extra):
        super().__init__(message, **extra)


# ------------------------- Policy Related Domain Errors -------------------------
class PolicyViolationError(PasswordError):
    """Raised when a policy fails checks."""

    def __init__(self, message: str, policy_name: str | None = None, **extra):
        super().__init__(message, policy=policy_name, **extra)
