from domain.interfaces.password_hasher import PasswordHasherInterface
from domain.value_objects.hashed_password import HashedPasswordVo


class VerifyPassword:
    def __init__(self, hasher: PasswordHasherInterface):
        self._hasher = hasher

    def execute(self, password: str, hashed: HashedPasswordVo) -> bool:
        if not password:
            return False
        return self._hasher.verify(password, hashed)
