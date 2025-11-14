from domain.entities.jwt_token import JwtEntity
from domain.exceptions.domain_errors import JwtInvalidError
from domain.interfaces.jwt_factory import JwtFactoryInterface
from domain.ports.services.jwt import JwtServicePort
from domain.value_objects.identifiers import UUIDVo
from domain.value_objects.jwt_type import JwtTypeVo


class ValidateJwt:
    """Validate and decode JWTs."""

    def __init__(self, service: JwtServicePort, factory: JwtFactoryInterface):
        self._service = service
        self._factory = factory

    def validate_access_token(
        self, token: str, subject: UUIDVo | None = None
    ) -> JwtEntity:
        payload, headers_dict = self._service.decode(token)
        token_entity = self._factory.from_decoded(payload, headers_dict)

        if token_entity.claims.typ != JwtTypeVo.ACCESS:
            raise JwtInvalidError("Token is not an access token")

        if subject and token_entity.claims.sub != subject:
            raise JwtInvalidError("Token subject does not match")

        if token_entity.is_expired():
            raise JwtInvalidError("Token is expired")

        return token_entity

    def validate_refresh_token(
        self, token: str, subject: UUIDVo | None = None
    ) -> JwtEntity:
        payload, headers_dict = self._service.decode(token)
        token_entity = self._factory.from_decoded(payload, headers_dict)

        if token_entity.claims.typ != JwtTypeVo.REFRESH:
            raise JwtInvalidError("Token is not a refresh token")

        if subject and token_entity.claims.sub != subject:
            raise JwtInvalidError("Token subject does not match")

        if token_entity.is_expired():
            raise JwtInvalidError("Token is expired")

        return token_entity
