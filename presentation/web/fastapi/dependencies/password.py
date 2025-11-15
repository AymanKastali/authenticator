from functools import lru_cache

from infrastructure.services.password.pwdlib_hasher import PwdLibPasswordHasher


@lru_cache
def pwdlib_hasher_dependency() -> PwdLibPasswordHasher:
    return PwdLibPasswordHasher()


# @lru_cache
# def password_hasher_dependency() -> HashPassword:
#     """Provide password hasher implementation."""
#     hasher = PwdLibPasswordHasher()
#     return HashPassword(hasher=hasher)


# @lru_cache
# def password_verifier_dependency() -> VerifyPassword:
#     """Provide password verifier implementation."""
#     hasher = PwdLibPasswordHasher()
#     return VerifyPassword(hasher=hasher)
