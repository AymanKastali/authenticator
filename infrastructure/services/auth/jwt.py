from typing import Any, Mapping

from jwt import (
    ExpiredSignatureError,
    InvalidTokenError,
    decode,
    encode,
    get_unverified_header,
)

from domain.ports.services.jwt import JwtServicePort
from infrastructure.config.jwt import JwtConfig
from infrastructure.exceptions.adapters_errors import (
    JwtExpiredError,
    JwtInvalidError,
)


class JwtService(JwtServicePort):
    def __init__(self, config: JwtConfig):
        self._config = config

    # ------------------------- Sign -------------------------
    def encode(
        self, claims: Mapping[str, Any], headers: Mapping[str, Any]
    ) -> str:
        private_key: str = self._config.private_key.get_secret_value()
        algorithm: str = headers.get("alg", self._config.algorithm)

        return encode(
            payload=dict(claims),
            key=private_key,
            algorithm=algorithm,
            headers=dict(headers),
        )

    # ------------------------- Decode -------------------------
    def decode(self, token: str) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
        public_key: str = self._config.public_key.get_secret_value()
        audience: str = self._config.audience
        issuer: str = self._config.issuer
        algorithm: str = self._config.algorithm
        leeway: int = self._config.leeway

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
            claims = decode(
                jwt=token,
                key=public_key,
                algorithms=[algorithm],
                audience=audience,
                issuer=issuer,
                leeway=leeway,
                options=options,
            )
            headers = get_unverified_header(token)
            return claims, headers
        except ExpiredSignatureError as e:
            raise JwtExpiredError() from e
        except InvalidTokenError as e:
            raise JwtInvalidError(message=str(e)) from e
