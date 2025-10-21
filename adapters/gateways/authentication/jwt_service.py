from jwt import PyJWTError, decode, encode

from adapters.utils.time_utils import (
    expires_after_days,
    expires_after_minutes,
    utc_now,
)
from application.ports.jwt_token_service import JwtTokenServicePort
from domain.config.config_models import JwtConfig
from domain.value_objects.jwt_claims import JwtClaims
from domain.value_objects.jwt_payload import JwtPayload


class JwtService(JwtTokenServicePort):
    def __init__(self, jwt_cfg: JwtConfig):
        self.jwt_cfg = jwt_cfg

    def generate_access_token(
        self, user_id: str, claims: JwtClaims | None = None
    ) -> str:
        claims = claims or JwtClaims()
        now = utc_now()
        payload = JwtPayload(
            sub=user_id,
            iat=now,
            exp=expires_after_minutes(
                self.jwt_cfg.access_token_expiration_minutes
            ),
            type="access",
            roles=claims.roles or [],
            email=claims.email,
            username=claims.username,
            iss=claims.issuer or self.jwt_cfg.issuer,
            aud=claims.audience or self.jwt_cfg.audience,
            nbf=claims.not_before or now,  # use client-provided nbf if given
        )
        return encode(
            payload.to_dict(),
            self.jwt_cfg.secret_key,
            algorithm=self.jwt_cfg.algorithm,
        )

    def generate_refresh_token(
        self, user_id: str, claims: JwtClaims | None = None
    ) -> str:
        claims = claims or JwtClaims()
        now = utc_now()
        payload = JwtPayload(
            sub=user_id,
            iat=now,
            exp=expires_after_days(self.jwt_cfg.refresh_token_expiration_days),
            type="refresh",
            roles=claims.roles or [],
            email=claims.email,
            username=claims.username,
            iss=claims.issuer or self.jwt_cfg.issuer,
            aud=claims.audience or self.jwt_cfg.audience,
            nbf=claims.not_before or now,  # use client-provided nbf if given
        )
        return encode(
            payload.to_dict(),
            self.jwt_cfg.secret_key,
            algorithm=self.jwt_cfg.algorithm,
        )

    def verify_access_token(self, token: str) -> JwtPayload | None:
        return self._verify_token(token, expected_type="access")

    def verify_refresh_token(self, token: str) -> JwtPayload | None:
        return self._verify_token(token, expected_type="refresh")

    def _verify_token(
        self,
        token: str,
        expected_type: str,
        leeway: int = 5,  # allow 5 seconds clock skew
    ) -> JwtPayload | None:
        try:
            payload_dict = decode(
                token,
                self.jwt_cfg.secret_key,
                algorithms=[self.jwt_cfg.algorithm],
                audience=self.jwt_cfg.audience,
                issuer=self.jwt_cfg.issuer,
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_nbf": True,
                    "require": ["sub", "iat", "exp", "type"],
                },
                leeway=leeway,
            )

            payload = JwtPayload(**payload_dict)

            # Ensure token type matches (access/refresh)
            if payload.type != expected_type:
                return None

            return payload

        except (PyJWTError, TypeError, ValueError):
            return None
