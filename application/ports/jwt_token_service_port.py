from abc import ABC, abstractmethod

from application.dto.jwt_dto import JwtTokenPayloadDto


class JwtTokenServicePort(ABC):
    """Port for token generation and verification."""

    @abstractmethod
    def sign(self, payload: JwtTokenPayloadDto) -> str: ...

    @abstractmethod
    def verify(self, token: str) -> JwtTokenPayloadDto: ...
