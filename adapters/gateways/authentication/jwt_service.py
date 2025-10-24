from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode

from adapters.config.jwt_config import JwtConfig
from application.dto.jwt_dto import JwtTokenPayloadDTO
from application.ports.jwt_token_service_port import JwtTokenServicePort
from domain.entities.jwt_token_payload import JwtTokenPayload


class JwtService(JwtTokenServicePort):
    def __init__(self, jwt_cfg: JwtConfig):
        self.jwt_cfg = jwt_cfg

    def sign(self, payload: JwtTokenPayload) -> str:
        token = encode(
            payload=JwtTokenPayloadDTO.entity_to_dict(payload),
            key=self.jwt_cfg.secret_key,
            algorithm=self.jwt_cfg.algorithm,
        )
        return token

    def verify(self, token: str, subject: str | None = None) -> JwtTokenPayload:
        try:
            options = {
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iat": True,
                "verify_aud": self.jwt_cfg.audience is not None,
                "verify_iss": self.jwt_cfg.issuer is not None,
            }

            decoded = decode(
                jwt=token,
                key=self.jwt_cfg.secret_key,
                algorithms=[self.jwt_cfg.algorithm],
                audience=self.jwt_cfg.audience
                if self.jwt_cfg.audience
                else None,
                issuer=self.jwt_cfg.issuer if self.jwt_cfg.issuer else None,
                subject=subject,
                leeway=self.jwt_cfg.leeway,
                options=options,
            )
        except ExpiredSignatureError as exc:
            raise Exception("Token expired") from exc
        except InvalidTokenError as exc:
            print("exc: ", exc)
            raise Exception("Invalid token") from exc

        return JwtTokenPayloadDTO.dict_to_entity(decoded)
