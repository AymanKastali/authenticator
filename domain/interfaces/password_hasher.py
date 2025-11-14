from abc import ABC, abstractmethod

from domain.value_objects.hashed_password import HashedPasswordVo


class PasswordHasherInterface(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        pass

    @abstractmethod
    def verify(self, password: str, hashed: HashedPasswordVo) -> bool:
        pass
