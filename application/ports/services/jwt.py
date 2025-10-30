from abc import ABC, abstractmethod

from application.dto.auth.jwt.token import JwtPayloadDto


class JwtServicePort(ABC):
    """Port for token generation and verification."""

    @abstractmethod
    def sign(self, payload: JwtPayloadDto) -> str: ...

    @abstractmethod
    def verify(
        self, token: str, subject: str | None = None
    ) -> JwtPayloadDto: ...

    @abstractmethod
    def verify_refresh_token(self, token: str) -> JwtPayloadDto: ...
