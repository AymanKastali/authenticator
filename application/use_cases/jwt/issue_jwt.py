from application.mappers.jwt import JwtMapper
from application.ports.services.jwt import JwtServicePort
from domain.entities.jwt_token import JwtEntity
from domain.entities.user import UserEntity
from domain.interfaces.jwt_factory import JwtFactoryInterface


class IssueJwtUseCase:
    def __init__(self, service: JwtServicePort, factory: JwtFactoryInterface):
        self._service = service
        self._factory = factory

    def issue_access_token(self, user: UserEntity) -> str:
        token: JwtEntity = self._factory.create_access_token(user)
        token_dicts: dict = JwtMapper.entity_to_dict(token)
        return self._service.encode(
            claims=token_dicts["claims"], headers=token_dicts["headers"]
        )

    def issue_refresh_token(self, user: UserEntity) -> str:
        token: JwtEntity = self._factory.create_refresh_token(user)
        token_dicts: dict = JwtMapper.entity_to_dict(token)
        return self._service.encode(
            claims=token_dicts["claims"], headers=token_dicts["headers"]
        )
