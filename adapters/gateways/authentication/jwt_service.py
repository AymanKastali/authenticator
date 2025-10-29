from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode

from adapters.config.jwt import JwtConfig
from adapters.exceptions.adapters_errors import JWTExpiredError, JWTInvalidError
from application.dto.auth.jwt.token import JwtTokenPayloadDto
from application.mappers.jwt import JwtTokenPayloadMapper
from application.ports.services.jwt import JwtServicePort


class JwtService(JwtServicePort):
    def __init__(self, jwt_cfg: JwtConfig):
        self.jwt_cfg = jwt_cfg

    def sign(self, payload: JwtTokenPayloadDto) -> str:
        token = encode(
            payload=JwtTokenPayloadMapper.to_dict_from_dto(payload),
            key=self.jwt_cfg.secret_key.get_secret_value(),
            algorithm=self.jwt_cfg.algorithm,
        )
        return token

    def verify(
        self, token: str, subject: str | None = None
    ) -> JwtTokenPayloadDto:
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

        return JwtTokenPayloadMapper.to_dto_from_dict(decoded)

    def verify_refresh_token(self, token: str) -> JwtTokenPayloadDto:
        jwt_token_payload_dto: JwtTokenPayloadDto = self.verify(token)
        if jwt_token_payload_dto.typ != "REFRESH":
            raise JWTInvalidError(message="Token type must be 'refresh'")
        return jwt_token_payload_dto
