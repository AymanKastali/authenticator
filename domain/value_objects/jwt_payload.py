from dataclasses import dataclass, field
from typing import Self

from domain.interfaces.policy import PolicyInterface
from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.email import EmailVo
from domain.value_objects.identifiers import UUIDVo
from domain.value_objects.jwt_type import JwtTypeVo
from domain.value_objects.role import RoleVo


@dataclass(frozen=True, slots=True, kw_only=True)
class JwtPayloadVo:
    """Represents JWT claims as a Value Object with strong validation and modern Python style."""

    sub: UUIDVo
    typ: JwtTypeVo
    exp: DateTimeVo
    jti: UUIDVo
    iat: DateTimeVo
    nbf: DateTimeVo
    iss: str | None = None
    aud: str | None = None
    email: EmailVo | None = None
    username: str | None = None
    roles: list[RoleVo] = field(default_factory=list)

    def __post_init__(self):
        self.validate()

    # ----------------- Validation Methods -----------------
    def validate(self) -> None:
        """Run all validations."""
        self._validate_sub()
        self._validate_typ()
        self._validate_exp()
        self._validate_iat()
        self._validate_nbf()
        self._validate_roles()

    def _validate_sub(self) -> None:
        if not isinstance(self.sub, UUIDVo):
            raise TypeError("`sub` must be a UUIDVo instance")

    def _validate_typ(self) -> None:
        if not isinstance(self.typ, JwtTypeVo):
            raise TypeError("`typ` must be a JwtTypeVo instance")

    def _validate_exp(self) -> None:
        if not isinstance(self.exp, DateTimeVo):
            raise TypeError("`exp` must be a DateTimeVo instance")
        if self.exp.is_before(self.iat):
            raise ValueError("`exp` must be after `iat`")

    def _validate_iat(self) -> None:
        if not isinstance(self.iat, DateTimeVo):
            raise TypeError("`iat` must be a DateTimeVo instance")
        self.iat.ensure_not_in_future()

    def _validate_nbf(self) -> None:
        if self.nbf is None:
            return
        if not isinstance(self.nbf, DateTimeVo):
            raise TypeError("`nbf` must be a DateTimeVo instance")
        if self.nbf.is_before(self.iat):
            raise ValueError("`nbf` cannot be before `iat`")
        if self.nbf.is_after(self.exp):
            raise ValueError("`nbf` cannot be after `exp`")

    def _validate_roles(self) -> None:
        if not all(isinstance(role, RoleVo) for role in self.roles):
            raise TypeError("All `roles` must be RoleVo instances")

    # ----------------- Factory Method -----------------
    @classmethod
    def create(
        cls,
        *,
        sub: UUIDVo,
        typ: JwtTypeVo,
        exp: int,
        roles: list[RoleVo] | None = None,
        email: EmailVo | None = None,
        username: str | None = None,
        iss: str | None = None,
        aud: str | None = None,
        nbf: DateTimeVo | None = None,
        policies: list[PolicyInterface],
    ) -> Self:
        """Factory for safely constructing a new payload VO."""
        jti = UUIDVo.new()
        now: DateTimeVo = DateTimeVo.now()
        expiry: DateTimeVo = now.expires_after(seconds=exp)
        roles = roles or []
        payload = cls(
            jti=jti,
            sub=sub,
            typ=typ,
            exp=expiry,
            roles=roles,
            email=email,
            username=username,
            iss=iss,
            aud=aud,
            iat=now,
            nbf=nbf or now,
        )
        if policies:
            for policy in policies:
                policy.enforce(payload)
        return payload

    # ----------------- Serialization -----------------
    def to_dict(self) -> dict[str, object]:
        nbf: float | None = self.nbf.to_timestamp() if self.nbf else None
        roles: list[str] = [r.value for r in self.roles]
        email: str | None = self.email.to_string() if self.email else None
        return {
            "sub": self.sub.to_string(),
            "typ": self.typ.value,
            "exp": self.exp.to_timestamp(),
            "jti": self.jti.to_string(),
            "iat": self.iat.to_timestamp(),
            "nbf": nbf,
            "iss": self.iss,
            "aud": self.aud,
            "roles": roles,
            "email": email,
            "username": self.username,
        }

    # ----------------- Convenience -----------------
    def is_expired(self) -> bool:
        """Quick check if the token is expired."""
        return self.exp.is_past()
