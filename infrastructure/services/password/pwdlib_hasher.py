from pwdlib import PasswordHash

from domain.interfaces.password_hasher import PasswordHasherInterface
from domain.value_objects.hashed_password import HashedPasswordVo


class PwdLibPasswordHasher(PasswordHasherInterface):
    def __init__(self):
        self._engine: PasswordHash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self._engine.hash(password)

    def verify(self, password: str, hashed: HashedPasswordVo) -> bool:
        return self._engine.verify(password, hashed.to_string())
