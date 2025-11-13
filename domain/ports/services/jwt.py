from abc import ABC, abstractmethod

from domain.entities.auth.jwt.token import JwtEntity
from domain.value_objects.identifiers import UUIDVo


class JwtServicePort(ABC):
    """Port for token generation and verification."""

    @abstractmethod
    def sign_token(self, token: JwtEntity) -> str: ...

    @abstractmethod
    def verify_token(
        self, token: str, subject: UUIDVo | None = None
    ) -> JwtEntity: ...

    @abstractmethod
    def verify_refresh_token(
        self, token: str, subject: UUIDVo | None = None
    ) -> JwtEntity: ...
