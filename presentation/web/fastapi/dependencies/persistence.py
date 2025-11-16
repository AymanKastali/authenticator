from application.ports.repositories.session import SessionRepositoryPort
from application.ports.repositories.user import UserRepositoryPort
from infrastructure.gateways.persistence.in_memory.providers import (
    provide_session_repository,
    provide_user_repository,
)


def in_memory_user_repository() -> UserRepositoryPort:
    return provide_user_repository()


def in_memory_session_repository() -> SessionRepositoryPort:
    return provide_session_repository()
