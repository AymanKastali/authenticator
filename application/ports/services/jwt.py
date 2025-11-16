from abc import ABC, abstractmethod
from typing import Any, Mapping


class JwtServicePort(ABC):
    """
    Port interface for JWT encoding and decoding.

    This is an infrastructure-agnostic abstraction.
    The domain layer should not depend on the JWT library directly.
    """

    @abstractmethod
    def encode(
        self, claims: Mapping[str, Any], headers: Mapping[str, Any]
    ) -> str: ...

    @abstractmethod
    def decode(
        self, token: str
    ) -> tuple[Mapping[str, Any], Mapping[str, Any]]: ...
