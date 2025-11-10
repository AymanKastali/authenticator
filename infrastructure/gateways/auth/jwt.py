from typing import Any

from jwt import (
    ExpiredSignatureError,
    InvalidTokenError,
    decode,
    encode,
    get_unverified_header,
)

from application.mappers.jwt import JwtMapper
from domain.entities.auth.jwt.token import JwtEntity
from domain.ports.services.jwt import JwtServicePort
from domain.value_objects.jwt_header import JwtHeaderVo
from domain.value_objects.jwt_header_algorithm import JwtHeaderAlgorithmVo
from domain.value_objects.jwt_payload import JwtPayloadVo
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
    def sign(
        self, payload: JwtPayloadVo, headers: JwtHeaderVo | None = None
    ) -> JwtEntity:
        """Sign a payload and return a JwtEntity."""
        headers = headers or self._create_default_headers()
        token: str = self._encode_token(payload, headers)
        return JwtEntity.create_signed(
            payload=payload, signature=token, headers=headers
        )

    def _create_default_headers(self) -> JwtHeaderVo:
        """Create default headers based on config."""
        return JwtHeaderVo.create(
            alg=JwtHeaderAlgorithmVo.from_string(self.jwt_cfg.algorithm)
        )

    def _encode_token(self, payload: JwtPayloadVo, headers: JwtHeaderVo) -> str:
        """Encode the payload and headers into a JWT string."""
        payload_dict: dict = payload.to_primitives()
        secret_key: str = self.jwt_cfg.secret_key.get_secret_value()
        algorithm: str = headers.alg or self.jwt_cfg.algorithm
        headers_dict: dict = headers.to_primitives()

        return encode(
            payload=payload_dict,
            key=secret_key,
            algorithm=algorithm,
            headers=headers_dict,
        )

    # ------------------------- Verify -------------------------
    def verify(
        self,
        token: str,
        subject: str | None = None,
        expected_headers: JwtHeaderVo | None = None,
    ) -> JwtPayloadVo:
        """Verify a token and return its payload."""
        headers_vo: JwtHeaderVo = self._extract_and_validate_headers(
            token, expected_headers
        )
        payload_dict: dict[str, Any] = self._decode_token(
            token, headers_vo, subject
        )
        return JwtMapper.to_payload_vo_from_dict(payload_dict)

    def verify_refresh_token(
        self,
        token: str,
        subject: str | None = None,
        expected_headers: JwtHeaderVo | None = None,
    ) -> JwtPayloadVo:
        """Verify a refresh token, including headers and type."""
        payload_vo: JwtPayloadVo = self.verify(token, subject, expected_headers)
        self._ensure_refresh_token(payload_vo)
        return payload_vo

    # ------------------------- Header Extraction & Validation -------------------------
    def _extract_and_validate_headers(
        self, token: str, expected_headers: JwtHeaderVo | None = None
    ) -> JwtHeaderVo:
        """Extract headers from token and optionally validate against expected headers."""
        raw_headers: dict[str, Any] = get_unverified_header(token)
        alg_value: Any | None = raw_headers.get("alg")
        if not isinstance(alg_value, str) or not alg_value.strip():
            raise JwtInvalidError("JWT header missing or invalid 'alg'")

        headers_vo = JwtHeaderVo(
            alg=JwtHeaderAlgorithmVo.from_string(alg_value),
            typ=raw_headers.get("typ", "JWT"),
            kid=raw_headers.get("kid"),
        )

        if expected_headers:
            self._assert_expected_headers(headers_vo, expected_headers)

        return headers_vo

    def _assert_expected_headers(
        self, actual: JwtHeaderVo, expected: JwtHeaderVo
    ) -> None:
        """Ensure that actual headers match expected headers."""
        if actual.alg != expected.alg:
            raise JwtInvalidError(
                message=f"Unexpected algorithm in token: {actual.alg}"
            )
        if expected.kid and actual.kid != expected.kid:
            raise JwtInvalidError(
                message=f"Unexpected key ID in token: {actual.kid}"
            )

    # ------------------------- Decode -------------------------
    def _decode_token(
        self, token: str, headers_vo: JwtHeaderVo, subject: str | None = None
    ) -> dict[str, Any]:
        """Decode the JWT payload using headers and config."""
        secret_key: str = self.jwt_cfg.secret_key.get_secret_value()
        algorithm: str = headers_vo.alg.value
        audience: str | None = self.jwt_cfg.audience or None
        issuer: str | None = self.jwt_cfg.issuer or None
        leeway: int = self.jwt_cfg.leeway

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
                key=secret_key,
                algorithms=[algorithm],
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

    # ------------------------- Refresh Token Validation -------------------------
    def _ensure_refresh_token(self, payload: JwtPayloadVo) -> None:
        """Ensure the token is a refresh token."""
        if payload.typ.value != JwtTypeVo.REFRESH.value:
            raise JwtInvalidError(
                message=f"Token type must be {JwtTypeVo.REFRESH.value}"
            )
