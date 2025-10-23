from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ItemResponseModel[T](BaseModel):
    status_code: int = 200
    message: str | None = None
    data: T | None = None

    @classmethod
    def build(
        cls,
        data: T | None,
        message: str | None = None,
        status_code: int = 200,
    ) -> "ItemResponseModel[T]":
        return cls(
            data=data,
            message=message,
            status_code=status_code,
        )
