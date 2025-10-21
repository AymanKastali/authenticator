from abc import ABC, abstractmethod

from domain.value_objects.jwt_claims import JwtClaims
from domain.value_objects.jwt_payload import JwtPayload


class JwtTokenServicePort(ABC):
    """Port for token generation and verification."""

    @abstractmethod
    def generate_access_token(
        self, user_id: str, claims: JwtClaims | None = None
    ) -> str: ...

    @abstractmethod
    def generate_refresh_token(
        self, user_id: str, claims: JwtClaims | None = None
    ) -> str: ...

    @abstractmethod
    def verify_access_token(self, token: str) -> JwtPayload | None: ...

    @abstractmethod
    def verify_refresh_token(self, token: str) -> JwtPayload | None: ...
