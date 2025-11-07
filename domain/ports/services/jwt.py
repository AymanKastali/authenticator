from abc import ABC, abstractmethod

from domain.entities.auth.jwt.token import JwtEntity
from domain.value_objects.jwt_payload import JwtPayloadVo


class JwtServicePort(ABC):
    """Port for token generation and verification."""

    @abstractmethod
    def sign(self, payload: JwtPayloadVo) -> JwtEntity: ...

    @abstractmethod
    def verify(
        self, token: str, subject: str | None = None
    ) -> JwtPayloadVo: ...

    @abstractmethod
    def verify_refresh_token(
        self, token: str, subject: str | None = None
    ) -> JwtPayloadVo: ...
