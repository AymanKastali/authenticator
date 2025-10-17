from abc import ABC, abstractmethod


class TokenServicePort(ABC):
    """Port for token generation and verification."""

    @abstractmethod
    def generate_token(self, user_id: str) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> str | None:
        pass
