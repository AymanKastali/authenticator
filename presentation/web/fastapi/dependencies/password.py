from functools import lru_cache

from domain.interfaces.policy import PolicyInterface
from domain.services.password.hash import HashPassword
from domain.services.password.verify import VerifyPassword
from infrastructure.services.password.pwdlib_hasher import PwdLibPasswordHasher
from presentation.web.fastapi.dependencies.policy import (
    password_policies,
)


@lru_cache
def password_hasher_dependency() -> HashPassword:
    """Provide password hasher implementation."""
    hasher = PwdLibPasswordHasher()
    policies: list[PolicyInterface] = password_policies()
    return HashPassword(hasher=hasher, policies=policies)


@lru_cache
def password_verifier_dependency() -> VerifyPassword:
    """Provide password verifier implementation."""
    hasher = PwdLibPasswordHasher()
    return VerifyPassword(hasher=hasher)
