from presentation.exceptions.error_codes import DeliveryErrorCodeEnum
from shared.utils.error_data import ErrorData, ErrorDetails


class DeliveryError(Exception):
    """
    Base class for delivery layer errors (HTTP / transport layer).
    """

    code: DeliveryErrorCodeEnum = DeliveryErrorCodeEnum.GENERAL

    def __init__(self, message: str | None = None, **extra):
        self.message = message or "An unexpected delivery error occurred."
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


class RequestParsingError(DeliveryError):
    code = DeliveryErrorCodeEnum.REQUEST_PARSING_FAILED

    def __init__(
        self, field_name: str | None = None, message: str | None = None, **extra
    ):
        message = message or f"Failed to parse request field '{field_name}'."
        super().__init__(message, field_name=field_name, **extra)


class ResponseSerializationError(DeliveryError):
    code = DeliveryErrorCodeEnum.RESPONSE_SERIALIZATION_FAILED

    def __init__(self, message: str | None = None, **extra):
        message = message or "Failed to serialize response."
        super().__init__(message, **extra)
