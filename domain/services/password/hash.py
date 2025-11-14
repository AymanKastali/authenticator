from domain.interfaces.password_hasher import PasswordHasherInterface
from domain.interfaces.policy import PolicyInterface
from domain.value_objects.hashed_password import HashedPasswordVo


class HashPassword:
    def __init__(
        self, hasher: PasswordHasherInterface, policies: list[PolicyInterface]
    ):
        self._hasher = hasher
        self._policies = policies

    def execute(self, password: str) -> HashedPasswordVo:
        for policy in self._policies:
            policy.enforce(password)
        hashed: str = self._hasher.hash(password)
        return HashedPasswordVo.from_string(hashed)
