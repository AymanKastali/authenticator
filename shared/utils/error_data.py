from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ErrorDetails:
    code: str
    message: str
    extra: dict[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class ErrorData:
    """Reusable structured error representation."""

    error: str
    details: ErrorDetails

    def to_dict(self) -> dict:
        base = {
            "error": self.error,
            "details": {
                "code": self.details.code,
                "message": self.details.message,
            },
        }
        if self.details.extra:
            base["details"].update(self.details.extra)
        return base
