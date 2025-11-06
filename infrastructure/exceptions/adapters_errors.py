from infrastructure.exceptions.error_codes import AdaptersErrorCodeEnum
from shared.utils.error_data import ErrorData, ErrorDetails


class AdaptersError(Exception):
    """
    Base class for adapter-level errors.
    Automatically handles:
      - code
      - message
      - optional extra data (cause, expired_at, etc.)
    """

    code: AdaptersErrorCodeEnum = AdaptersErrorCodeEnum.GENERAL

    def __init__(self, message: str | None = None, **extra):
        """
        Args:
            message: Human-readable error message.
            **extra: Optional extra metadata to include in the error.
        """
        self.message = message or "An unexpected adapter error occurred."
        self._extra = extra or {}
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """
        Convert to structured error dictionary using ErrorData/ErrorDetails.
        Automatically includes all extra metadata.
        """
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


class JWTExpiredError(AdaptersError):
    code = AdaptersErrorCodeEnum.JWT_EXPIRED

    def __init__(self, message: str | None = None):
        super().__init__(message or "JWT token has expired.")


class JWTInvalidError(AdaptersError):
    code = AdaptersErrorCodeEnum.JWT_INVALID

    def __init__(self, message: str | None = None):
        super().__init__(message or "JWT token is invalid or malformed.")


class DatabaseConnectionError(AdaptersError):
    code = AdaptersErrorCodeEnum.DB_CONNECTION

    def __init__(self, message: str | None = None):
        super().__init__(message or "Failed to connect to the database.")
