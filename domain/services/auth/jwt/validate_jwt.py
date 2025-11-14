from domain.entities.auth.jwt.token import JwtEntity
from domain.ports.services.jwt import JwtServicePort
from domain.value_objects.identifiers import UUIDVo


class ValidateJwt:
    """Validate and decode JWTs."""

    def __init__(self, jwt_service: JwtServicePort):
        self._jwt_service = jwt_service

    def validate_access_token(
        self, token: str, subject: UUIDVo | None = None
    ) -> JwtEntity:
        return self._jwt_service.verify_token(token, subject)

    def validate_refresh_token(
        self, token: str, subject: UUIDVo | None = None
    ) -> JwtEntity:
        return self._jwt_service.verify_refresh_token(token, subject)
