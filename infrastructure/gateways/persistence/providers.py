from functools import cache

from domain.ports.repositories.session import SessionRepositoryPort
from domain.ports.repositories.user import UserRepositoryPort
from infrastructure.gateways.persistence.in_memory.db.storage import (
    InMemorySessionStorage,
    InMemoryUserStorage,
)
from infrastructure.gateways.persistence.in_memory.repositories.in_memory_session_repository import (
    InMemorySessionRepository,
)
from infrastructure.gateways.persistence.in_memory.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)

# -----------------------
#  Singletons
# -----------------------
user_storage = InMemoryUserStorage()
session_storage = InMemorySessionStorage()


# -----------------------
#  Dependency Providers
# -----------------------
@cache
def provide_user_repository() -> UserRepositoryPort:
    """
    Returns a singleton user repository.
    Modern, explicit, FastAPI-friendly.
    """
    return InMemoryUserRepository(storage=user_storage)


@cache
def provide_session_repository() -> SessionRepositoryPort:
    """
    Returns a singleton session repository.
    """
    return InMemorySessionRepository(storage=session_storage)
