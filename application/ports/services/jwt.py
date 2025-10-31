from abc import ABC, abstractmethod

from application.dto.auth.jwt.payload import JwtPayloadDto
from application.dto.auth.jwt.token import JwtDto


class JwtServicePort(ABC):
    """Port for token generation and verification."""

    @abstractmethod
    def sign(self, payload: JwtPayloadDto) -> JwtDto: ...

    @abstractmethod
    def verify(self, token: str, subject: str | None = None) -> JwtDto: ...

    @abstractmethod
    def verify_refresh_token(self, token: str) -> JwtDto: ...
