from functools import lru_cache

from adapters.gateways.persistence.in_memory.repositories.in_memory_session_repository import (
    InMemorySessionRepository,
)
from adapters.gateways.persistence.in_memory.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)


@lru_cache()
def get_in_memory_user_repository() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@lru_cache()
def get_in_memory_session_repository() -> InMemorySessionRepository:
    return InMemorySessionRepository()
