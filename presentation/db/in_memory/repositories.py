from functools import lru_cache

from application.ports.repositories.session import SessionRepositoryPort
from domain.ports.repositories.user import UserRepositoryPort
from infrastructure.gateways.persistence.in_memory.repositories.in_memory_session_repository import (
    InMemorySessionRepository,
)
from infrastructure.gateways.persistence.in_memory.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)


@lru_cache(maxsize=1)
def get_in_memory_user_repository() -> UserRepositoryPort:
    return InMemoryUserRepository()


@lru_cache(maxsize=1)
def get_in_memory_session_repository() -> SessionRepositoryPort:
    return InMemorySessionRepository()
