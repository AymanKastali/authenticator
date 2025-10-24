from abc import ABC, abstractmethod

from domain.entities.jwt_token_payload import JwtTokenPayload


class JwtTokenServicePort(ABC):
    """Port for token generation and verification."""

    @abstractmethod
    def sign(self, payload: JwtTokenPayload) -> str: ...

    @abstractmethod
    def verify(self, token: str) -> JwtTokenPayload: ...
