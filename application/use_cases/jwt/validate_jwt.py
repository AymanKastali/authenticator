from application.ports.services.jwt import JwtServicePort
from domain.entities.jwt_token import JwtEntity
from domain.exceptions.domain_errors import JwtInvalidError
from domain.factories.value_objects.type import JwtTypeVoFactory
from domain.interfaces.jwt_factory import JwtFactoryInterface
from domain.value_objects.uuid_id import UUIDVo


class ValidateJwtUseCase:
    """Validate and decode JWTs."""

    def __init__(self, service: JwtServicePort, factory: JwtFactoryInterface):
        self._service = service
        self._factory = factory

    def execute(
        self, token: str, token_type: str, subject: UUIDVo | None = None
    ) -> JwtEntity:
        payload, headers_dict = self._service.decode(token)
        token_entity: JwtEntity = self._factory.from_decoded(
            payload, headers_dict
        )

        if (
            token_entity.claims.typ.value
            != JwtTypeVoFactory.create(token_type).value
        ):
            raise JwtInvalidError(f"Token is not an {token_type} token")

        if subject and token_entity.claims.sub != subject:
            raise JwtInvalidError("Token subject does not match")

        if token_entity.is_expired():
            raise JwtInvalidError("Token is expired")

        return token_entity
