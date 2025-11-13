from typing import Any

from jwt import (
    ExpiredSignatureError,
    InvalidTokenError,
    decode,
    encode,
    get_unverified_header,
)

from domain.entities.auth.jwt.token import JwtEntity
from domain.ports.services.jwt import JwtServicePort
from domain.value_objects.identifiers import UUIDVo
from domain.value_objects.jwt_claims import JwtClaimsVo
from domain.value_objects.jwt_header import JwtHeaderVo
from domain.value_objects.jwt_type import JwtTypeVo
from infrastructure.config.jwt import JwtConfig
from infrastructure.exceptions.adapters_errors import (
    JwtExpiredError,
    JwtInvalidError,
)


class JwtService(JwtServicePort):
    def __init__(self, jwt_cfg: JwtConfig):
        self.jwt_cfg = jwt_cfg

    # ------------------------- Sign -------------------------
    def sign_token(self, token: JwtEntity) -> str:
        """Encode the claims and headers into a JWT string."""
        payload: dict = token.claims.to_dict()
        private_key: str = self.jwt_cfg.private_key.get_secret_value()
        algorithm: str = token.headers.alg.value
        headers_dict: dict = token.headers.to_dict()

        return encode(
            payload=payload,
            key=private_key,
            algorithm=algorithm,
            headers=headers_dict,
        )

    # ------------------------- Verify -------------------------
    def verify_token(
        self, token: str, subject: UUIDVo | None = None
    ) -> JwtEntity:
        subject_string = subject.to_string() if subject else None
        claims_dict: dict[str, Any] = self._decode_token(
            token=token,
            algorithms=[self.jwt_cfg.algorithm],
            leeway=self.jwt_cfg.leeway,
            audience=self.jwt_cfg.audience,
            issuer=self.jwt_cfg.issuer,
            subject=subject_string,
        )
        claims_vo = JwtClaimsVo.from_dict(claims_dict)
        raw_headers: dict[str, Any] = get_unverified_header(token)
        headers_vo = JwtHeaderVo.from_dict(raw_headers)
        return JwtEntity.create(claims=claims_vo, headers=headers_vo)

    def verify_refresh_token(
        self, token: str, subject: UUIDVo | None = None
    ) -> JwtEntity:
        """Verify a refresh token, including headers and type."""
        token_entity: JwtEntity = self.verify_token(token, subject)
        if token_entity.claims.typ.value != JwtTypeVo.REFRESH.value:
            raise JwtInvalidError(
                message=f"Token type must be {JwtTypeVo.REFRESH.value}"
            )
        return token_entity

    # ------------------------- Decode -------------------------
    def _decode_token(
        self,
        token: str,
        algorithms: list[str],
        leeway: int,
        audience: str | None = None,
        issuer: str | None = None,
        subject: str | None = None,
    ) -> dict[str, Any]:
        """Decode the JWT claims using headers and config."""
        public_key: str = self.jwt_cfg.public_key.get_secret_value()

        options = {
            "require": ["exp", "iat"],
            "verify_signature": True,
            "verify_exp": True,
            "verify_nbf": True,
            "verify_iat": True,
            "verify_aud": bool(audience),
            "verify_iss": bool(issuer),
        }

        try:
            return decode(
                jwt=token,
                key=public_key,
                algorithms=algorithms,
                audience=audience,
                issuer=issuer,
                subject=subject,
                leeway=leeway,
                options=options,
            )
        except ExpiredSignatureError as e:
            raise JwtExpiredError() from e
        except InvalidTokenError as e:
            raise JwtInvalidError(message=str(e)) from e
