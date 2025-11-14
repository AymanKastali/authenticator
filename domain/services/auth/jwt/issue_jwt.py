from domain.entities.jwt_token import JwtEntity
from domain.entities.user import UserEntity
from domain.interfaces.jwt_factory import JwtFactoryInterface
from domain.ports.services.jwt import JwtServicePort


class IssueJwt:
    def __init__(self, service: JwtServicePort, factory: JwtFactoryInterface):
        self._service = service
        self._factory = factory

    def issue_access_token(self, user: UserEntity) -> str:
        token: JwtEntity = self._factory.create_access_token(user)
        return self._service.encode(
            claims=token.claims.to_dict(), headers=token.headers.to_dict()
        )

    def issue_refresh_token(self, user: UserEntity) -> str:
        token: JwtEntity = self._factory.create_refresh_token(user)
        return self._service.encode(
            claims=token.claims.to_dict(), headers=token.headers.to_dict()
        )
