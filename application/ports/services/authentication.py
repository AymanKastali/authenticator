from abc import ABC, abstractmethod

from application.dto.auth.jwt.auth_user import AuthUserDto


class AuthenticationServicePort(ABC):
    @abstractmethod
    def login(self, email: str, password: str) -> AuthUserDto: ...

    @abstractmethod
    def register(self, email: str, password: str) -> AuthUserDto: ...
