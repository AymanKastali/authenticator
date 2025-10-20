from abc import ABC, abstractmethod


class JwtTokenServicePort(ABC):
    """Port for token generation and verification."""

    @abstractmethod
    def generate_access_token(self, user_id: str) -> str: ...

    @abstractmethod
    def generate_refresh_token(self, user_id: str) -> str: ...

    @abstractmethod
    def verify_access_token(self, token: str) -> str | None: ...

    @abstractmethod
    def verify_refresh_token(self, token: str) -> str | None: ...
