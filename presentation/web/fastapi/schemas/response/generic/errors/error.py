from typing import Any

from pydantic import BaseModel


class ErrorResponseSchema(BaseModel):
    status_code: int
    error: str
    details: Any | None = None
