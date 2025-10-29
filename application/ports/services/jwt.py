from abc import ABC, abstractmethod

from application.dto.auth.jwt.token import JwtTokenPayloadDto


class JwtServicePort(ABC):
    """Port for token generation and verification."""

    @abstractmethod
    def sign(self, payload: JwtTokenPayloadDto) -> str: ...

    @abstractmethod
    def verify(
        self, token: str, subject: str | None = None
    ) -> JwtTokenPayloadDto: ...

    @abstractmethod
    def verify_refresh_token(self, token: str) -> JwtTokenPayloadDto: ...
