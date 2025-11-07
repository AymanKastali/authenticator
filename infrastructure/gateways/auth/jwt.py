from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode

from application.mappers.jwt import JwtMapper
from domain.entities.auth.jwt.token import JwtEntity
from domain.ports.services.jwt import JwtServicePort
from domain.value_objects.jwt_payload import JwtPayloadVo
from infrastructure.config.jwt import JwtConfig
from infrastructure.exceptions.adapters_errors import (
    JWTExpiredError,
    JWTInvalidError,
)


class JwtService(JwtServicePort):
    def __init__(self, jwt_cfg: JwtConfig):
        self.jwt_cfg = jwt_cfg

    def sign(self, payload: JwtPayloadVo) -> JwtEntity:
        """Sign a payload and return a JwtEntity."""
        headers = {"alg": self.jwt_cfg.algorithm, "typ": "JWT"}
        token_str = encode(
            payload=payload.to_primitives(),
            key=self.jwt_cfg.secret_key.get_secret_value(),
            algorithm=self.jwt_cfg.algorithm,
            headers=headers,
        )
        return JwtEntity.create_signed(
            payload=payload, signature=token_str, headers=headers
        )

    def verify(self, token: str, subject: str | None = None) -> JwtPayloadVo:
        """Verify a token and return its payload."""
        try:
            options = {
                "require": ["exp", "iat"],
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iat": True,
                "verify_aud": self.jwt_cfg.audience is not None,
                "verify_iss": self.jwt_cfg.issuer is not None,
            }

            decoded = decode(
                jwt=token,
                key=self.jwt_cfg.secret_key.get_secret_value(),
                algorithms=[self.jwt_cfg.algorithm],
                audience=self.jwt_cfg.audience
                if self.jwt_cfg.audience
                else None,
                issuer=self.jwt_cfg.issuer if self.jwt_cfg.issuer else None,
                subject=subject,
                leeway=self.jwt_cfg.leeway,
                options=options,
            )
        except ExpiredSignatureError as e:
            raise JWTExpiredError() from e
        except InvalidTokenError as e:
            raise JWTInvalidError(message=str(e)) from e
        return JwtMapper.to_payload_vo_from_dict(decoded)

    def verify_refresh_token(
        self, token: str, subject: str | None = None
    ) -> JwtPayloadVo:
        payload: JwtPayloadVo = self.verify(token, subject)
        if payload.typ.lower() != "refresh":
            raise JWTInvalidError(message="Token type must be 'refresh'")
        return payload
