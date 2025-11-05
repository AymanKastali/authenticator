from dataclasses import dataclass, field
from typing import Self

from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.email import EmailVo
from domain.value_objects.identifiers import UUIDIdVo
from domain.value_objects.jwt_type import JwtTypeVo
from domain.value_objects.role import RoleVo


@dataclass(frozen=True, slots=True, kw_only=True)
class JwtPayloadVo:
    """Represents JWT claims as a Value Object with strong validation and modern Python style."""

    sub: UUIDIdVo
    typ: JwtTypeVo
    exp: DateTimeVo
    jti: UUIDIdVo = field(default_factory=UUIDIdVo.new)
    iat: DateTimeVo = field(default_factory=DateTimeVo.now)
    nbf: DateTimeVo = field(default_factory=DateTimeVo.now)
    iss: str | None = None
    aud: str | None = None
    roles: list[RoleVo] = field(default_factory=list)
    email: EmailVo | None = None
    username: str | None = None

    def __post_init__(self):
        self.validate()

    # ----------------- Validation Methods -----------------
    def validate(self) -> None:
        """Run all validations."""
        self.validate_sub()
        self.validate_typ()
        self.validate_exp()
        self.validate_iat()
        self.validate_nbf()
        self.validate_roles()

    def validate_sub(self) -> None:
        if not isinstance(self.sub, UUIDIdVo):
            raise TypeError("`sub` must be a UUIDIdVo instance")

    def validate_typ(self) -> None:
        if not isinstance(self.typ, JwtTypeVo):
            raise TypeError("`typ` must be a JwtTypeVo instance")

    def validate_exp(self) -> None:
        if not isinstance(self.exp, DateTimeVo):
            raise TypeError("`exp` must be a DateTimeVo instance")
        if self.exp.is_before(self.iat):
            raise ValueError("`exp` must be after `iat`")

    def validate_iat(self) -> None:
        if not isinstance(self.iat, DateTimeVo):
            raise TypeError("`iat` must be a DateTimeVo instance")
        if self.iat.is_future():
            raise ValueError("`iat` cannot be in the future")

    def validate_nbf(self) -> None:
        if not isinstance(self.nbf, DateTimeVo):
            raise TypeError("`nbf` must be a DateTimeVo instance")
        if self.nbf.is_future():
            raise ValueError("`nbf` cannot be in the future")

    def validate_roles(self) -> None:
        if not all(isinstance(role, RoleVo) for role in self.roles):
            raise TypeError("All `roles` must be RoleVo instances")

    # ----------------- Factory Method -----------------
    @classmethod
    def create(
        cls,
        *,
        sub: UUIDIdVo,
        typ: JwtTypeVo,
        expires_after_seconds: float,
        roles: list[RoleVo] | None = None,
        email: EmailVo | None = None,
        username: str | None = None,
        iss: str | None = None,
        aud: str | None = None,
        nbf: DateTimeVo | None = None,
    ) -> Self:
        """Factory for safely constructing a new payload VO."""
        now = DateTimeVo.now()
        exp = now.expires_after(seconds=expires_after_seconds)
        return cls(
            sub=sub,
            typ=typ,
            exp=exp,
            roles=roles or [],
            email=email,
            username=username,
            iss=iss,
            aud=aud,
            nbf=nbf or DateTimeVo.now(),
        )

    # ----------------- Serialization -----------------
    def to_primitives(self) -> dict[str, object]:
        """Return a primitive dictionary for JWT encoding or persistence."""
        return {
            "sub": str(self.sub),
            "typ": self.typ.value,
            "exp": self.exp.to_timestamp(),
            "jti": self.jti.to_string(),
            "iat": self.iat.to_timestamp(),
            "nbf": self.nbf.to_timestamp(),
            "iss": self.iss,
            "aud": self.aud,
            "roles": [r.value for r in self.roles],
            "email": self.email.to_string() if self.email else None,
            "username": self.username,
        }

    # ----------------- Convenience -----------------
    def is_expired(self) -> bool:
        """Quick check if the token is expired."""
        return self.exp.is_past()
