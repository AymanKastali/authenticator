from functools import lru_cache

from adapters.gateways.persistence.in_memory.repositories.in_memory_session_repository import (
    InMemorySessionRepository,
)
from adapters.gateways.persistence.in_memory.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)
from application.ports.repositories.session import SessionRepositoryPort
from application.ports.repositories.user import UserRepositoryPort


@lru_cache(maxsize=1)
def get_in_memory_user_repository() -> UserRepositoryPort:
    return InMemoryUserRepository()


@lru_cache(maxsize=1)
def get_in_memory_session_repository() -> SessionRepositoryPort:
    return InMemorySessionRepository()
