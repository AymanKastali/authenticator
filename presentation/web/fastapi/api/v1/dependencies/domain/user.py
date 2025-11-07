from fastapi import Depends

from domain.ports.repositories.user import UserRepositoryPort
from domain.services.user import UserDomainService
from presentation.db.in_memory.repositories import get_in_memory_user_repository


def user_domain_service_dependency(
    user_repo: UserRepositoryPort = Depends(get_in_memory_user_repository),
) -> UserDomainService:
    return UserDomainService(user_repo)
