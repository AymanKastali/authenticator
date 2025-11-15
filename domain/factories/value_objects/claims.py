from domain.factories.value_objects.date_time import DateTimeVoFactory
from domain.factories.value_objects.email import EmailVoFactory
from domain.factories.value_objects.role import RoleVoFactory
from domain.factories.value_objects.type import JwtTypeVoFactory
from domain.factories.value_objects.uuid import UUIDVoFactory
from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.jwt_claims import JwtClaimsVo
from domain.value_objects.role import RoleVo


class JwtClaimsVoFactory:
    @classmethod
    def create(
        cls,
        token_type_str: str,
        lifetime_seconds: int,
        email_str: str,
        role_strs: list[str],
        issuer: str | None = None,
        audience: str | None = None,
    ) -> JwtClaimsVo:
        now = DateTimeVoFactory.now()
        jti = UUIDVoFactory.new()
        sub = UUIDVoFactory.new()
        exp = DateTimeVoFactory.expires_after(now, lifetime_seconds)

        email_vo = EmailVoFactory.create(email_str)
        roles_vo = [RoleVoFactory.from_string(r) for r in role_strs]
        token_type_vo = JwtTypeVoFactory.create(token_type_str)

        # ---------------------
        # VALIDATIONS (moved from VO)
        # ---------------------
        cls._validate_time_order(iat=now, nbf=now, exp=exp)
        cls._validate_roles(roles_vo)

        # Construct VO once validated
        return JwtClaimsVo(
            sub=sub,
            typ=token_type_vo,
            exp=exp,
            jti=jti,
            iat=now,
            nbf=now,
            email=email_vo,
            roles=roles_vo,
            iss=issuer,
            aud=audience,
            extras={},
            username=None,
        )

    @classmethod
    def from_dict(cls, data: dict) -> JwtClaimsVo:
        """Reconstruct a JwtClaimsVo from a dictionary."""
        return JwtClaimsVo(
            sub=UUIDVoFactory.from_string(data["sub"]),
            typ=JwtTypeVoFactory.create(data["typ"]),
            exp=DateTimeVoFactory.from_timestamp(data["exp"]),
            jti=UUIDVoFactory.from_string(data["jti"]),
            iat=DateTimeVoFactory.from_timestamp(data["iat"]),
            nbf=DateTimeVoFactory.from_timestamp(data["nbf"]),
            iss=data.get("iss"),
            aud=data.get("aud"),
            email=EmailVoFactory.from_string(data["email"])
            if data.get("email")
            else None,
            username=data.get("username"),
            roles=[RoleVo.from_string(r) for r in data.get("roles", [])],
            extras=data.get("extras", {}),
        )

    # ---------------------------
    # MINI VALIDATION HELPERS
    # ---------------------------
    @staticmethod
    def _validate_time_order(iat: DateTimeVo, nbf: DateTimeVo, exp: DateTimeVo):
        if exp.is_before(iat):
            raise ValueError("`exp` must be after `iat`")

        if nbf.is_before(iat):
            raise ValueError("`nbf` cannot be before `iat`")

        if nbf.is_after(exp):
            raise ValueError("`nbf` cannot be after `exp`")

    @staticmethod
    def _validate_roles(roles: list[RoleVo]):
        if not all(isinstance(role, RoleVo) for role in roles):
            raise TypeError("All roles must be instances of RoleVo")
