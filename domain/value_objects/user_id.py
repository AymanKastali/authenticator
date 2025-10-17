import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class UserId:
    value: str

    @staticmethod
    def new() -> "UserId":
        return UserId(str(uuid.uuid4()))
