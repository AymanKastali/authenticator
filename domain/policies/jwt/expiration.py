from domain.exceptions.domain_errors import PolicyViolationError
from domain.factories.value_objects.date_time import DateTimeVoFactory
from domain.interfaces.policy import PolicyInterface
from domain.value_objects.jwt_claims import JwtClaimsVo
from domain.value_objects.jwt_type import JwtTypeVo
from domain.value_objects.policy_description import PolicyDescriptionVo


class JwtExpirationPolicy(PolicyInterface):
    """Limits the maximum token expiration for JWTs."""

    def __init__(
        self,
        access_token_max_age_seconds: int,
        refresh_token_max_age_seconds: int,
    ):
        self.access_exp = access_token_max_age_seconds
        self.refresh_exp = refresh_token_max_age_seconds

    def enforce(self, target: JwtClaimsVo) -> None:
        now = DateTimeVoFactory.now()
        max_expiry = (
            self.access_exp
            if target.typ == JwtTypeVo.ACCESS
            else self.refresh_exp
        )
        allowed_exp = DateTimeVoFactory.expires_after(now, max_expiry)

        if target.exp.is_after(allowed_exp):
            raise PolicyViolationError(
                message=f"{target.typ.value} token expiry exceeds policy ({max_expiry}s)",
                policy_name="jwt_expiration",
            )

    def describe(self) -> PolicyDescriptionVo:
        return PolicyDescriptionVo(
            name="expiration",
            category="jwt",
            parameters={
                "access_token_max_age_seconds": self.access_exp,
                "refresh_token_max_age_seconds": self.refresh_exp,
            },
        )
