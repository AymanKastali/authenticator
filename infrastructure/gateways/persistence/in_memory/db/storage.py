from uuid import UUID

from domain.entities.session import SessionEntity
from domain.entities.user import UserEntity


class InMemoryUserStorage:
    def __init__(self) -> None:
        self.users: dict[UUID, UserEntity] = {}


class InMemorySessionStorage:
    def __init__(self) -> None:
        self.sessions: dict[UUID, SessionEntity] = {}
