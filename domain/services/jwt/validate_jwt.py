from domain.ports.services.jwt import JwtServicePort
from domain.value_objects.jwt_header import JwtHeaderVo
from domain.value_objects.jwt_payload import JwtPayloadVo


class ValidateJwt:
    """Validate and decode JWTs."""

    def __init__(self, jwt_service: JwtServicePort):
        self._jwt_service = jwt_service

    def access(
        self,
        token: str,
        subject: str | None = None,
        headers: JwtHeaderVo | None = None,
    ) -> JwtPayloadVo:
        return self._jwt_service.verify(token, subject, headers)

    def refresh(
        self,
        token: str,
        subject: str | None = None,
        headers: JwtHeaderVo | None = None,
    ) -> JwtPayloadVo:
        return self._jwt_service.verify_refresh_token(token, subject, headers)
