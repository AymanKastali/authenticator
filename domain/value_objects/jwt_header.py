from dataclasses import dataclass, field
from typing import Self

from domain.value_objects.jwt_header_algorithm import JwtHeaderAlgorithmVo

_HEADER_TYPE: str = "JWT"


@dataclass(frozen=True, slots=True, kw_only=True)
class JwtHeaderVo:
    """
    Represents JWT headers as a Value Object with strong typing and validation.

    Attributes:
        alg: The signing algorithm (enum), must be one of the allowed JWT algorithms.
        typ: Token type, defaults to "JWT".
        kid: Optional key ID for key rotation.
    """

    alg: JwtHeaderAlgorithmVo
    typ: str = field(default=_HEADER_TYPE)
    kid: str | None = field(default=None)

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        self._validate_alg()
        self._validate_typ()
        self._validate_kid()

    def _validate_alg(self):
        if not isinstance(self.alg, JwtHeaderAlgorithmVo):
            raise TypeError("alg must be JwtHeaderAlgorithmVo")

    def _validate_typ(self) -> None:
        if self.typ != _HEADER_TYPE:
            raise ValueError(f"Invalid JWT type: {self.typ}")

    def _validate_kid(self) -> None:
        if self.kid is not None and not self.kid.strip():
            raise ValueError("JWT 'kid' cannot be empty if provided")

    def to_dict(self) -> dict[str, str]:
        headers = {"alg": self.alg.value, "typ": self.typ}
        if self.kid is not None:
            headers["kid"] = self.kid
        return headers

    @classmethod
    def create(
        cls,
        *,
        alg: JwtHeaderAlgorithmVo,
        typ: str = _HEADER_TYPE,
        kid: str | None = None,
    ) -> Self:
        return cls(alg=alg, typ=typ, kid=kid)
