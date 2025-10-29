from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ListOutDto[T](BaseModel):
    status_code: int = 200
    message: str | None = None
    data: list[T] | None = None

    @classmethod
    def build(
        cls,
        data: list[T] | None = None,
        message: str | None = None,
        status_code: int = 200,
    ) -> "ListOutDto[T]":
        return cls(data=data, message=message, status_code=status_code)
