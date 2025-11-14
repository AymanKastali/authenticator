from abc import ABC, abstractmethod
from typing import Any, Mapping

from domain.entities.jwt_token import JwtEntity
from domain.entities.user import UserEntity


class JwtFactoryInterface(ABC):
    @abstractmethod
    def create_access_token(self, user: UserEntity) -> JwtEntity: ...

    @abstractmethod
    def create_refresh_token(self, user: UserEntity) -> JwtEntity: ...

    @abstractmethod
    def from_decoded(
        self,
        decoded_claims: Mapping[str, Any],
        decoded_headers: Mapping[str, Any],
    ) -> JwtEntity: ...
