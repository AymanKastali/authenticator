from application.exceptions.error_codes import ApplicationErrorCodeEnum
from shared.utils.error_data import ErrorData, ErrorDetails


class ApplicationError(Exception):
    """
    Base class for application-level errors.
    """

    code: ApplicationErrorCodeEnum = ApplicationErrorCodeEnum.GENERAL

    def __init__(self, message: str | None = None, **extra):
        self.message = message or "An unexpected application error occurred."
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


class ServiceExecutionError(ApplicationError):
    code = ApplicationErrorCodeEnum.SERVICE_EXECUTION_ERROR

    def __init__(self, service_name: str, message: str | None = None, **extra):
        message = message or f"Service '{service_name}' failed to execute."
        super().__init__(message, service=service_name, **extra)


class TransactionError(ApplicationError):
    code = ApplicationErrorCodeEnum.TRANSACTION_FAILED

    def __init__(
        self,
        transaction_id: str | None = None,
        message: str | None = None,
        **extra,
    ):
        message = message or "Transaction failed during execution."
        super().__init__(message, transaction_id=transaction_id, **extra)
