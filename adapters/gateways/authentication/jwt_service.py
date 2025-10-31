from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode

from adapters.config.jwt import JwtConfig
from adapters.exceptions.adapters_errors import JWTExpiredError, JWTInvalidError
from application.dto.auth.jwt.payload import JwtPayloadDto
from application.dto.auth.jwt.token import JwtDto
from application.mappers.jwt import JwtMapper
from application.ports.services.jwt import JwtServicePort


class JwtService(JwtServicePort):
    def __init__(self, jwt_cfg: JwtConfig):
        self.jwt_cfg = jwt_cfg

    def sign(self, payload: JwtPayloadDto) -> JwtDto:
        headers: dict = {"alg": self.jwt_cfg.algorithm, "typ": "JWT"}
        token_str: str = encode(
            payload=payload.__dict__,
            key=self.jwt_cfg.secret_key.get_secret_value(),
            algorithm=self.jwt_cfg.algorithm,
            headers=headers,
        )
        return JwtDto(payload=payload, headers=headers, signature=token_str)

    def verify(self, token: str, subject: str | None = None) -> JwtDto:
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

        payload_dto = JwtMapper.to_payload_dto_from_dict(decoded)
        headers = {
            "alg": self.jwt_cfg.algorithm,
            "typ": "JWT",
        }  # optionally extract from token
        return JwtDto(payload=payload_dto, headers=headers, signature=token)

    def verify_refresh_token(self, token: str) -> JwtDto:
        token_dto: JwtDto = self.verify(token)
        if token_dto.payload.typ != "REFRESH":
            raise JWTInvalidError(message="Token type must be 'refresh'")
        return token_dto
