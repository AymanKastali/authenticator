from application.dto.auth.jwt.token import JwtDto
from application.mappers.jwt import JwtMapper
from application.ports.services.jwt import JwtServicePort
from domain.entities.auth.jwt.token import JwtEntity
from domain.entities.user import UserEntity
from domain.utils.time import expires_after
from domain.value_objects.jwt_payload import JwtPayloadVo
from domain.value_objects.jwt_token_type import JwtTokenType


class JwtAuthService:
    """Responsible for signing and verifying JWTs."""

    def __init__(self, jwt_service: JwtServicePort):
        self._jwt_service = jwt_service

    def create_access_token(self, user: UserEntity) -> JwtEntity:
        payload_vo = JwtPayloadVo.create(
            sub=user.uid,
            email=user.email,
            typ=JwtTokenType.ACCESS,
            roles=list(user.roles),
            exp=expires_after(minutes=30),
        )
        payload_dto = JwtMapper.to_payload_dto_from_vo(payload_vo)
        jwt_dto: JwtDto = self._jwt_service.sign(payload_dto)
        token = JwtEntity.create_signed(
            payload=payload_vo, signature=jwt_dto.signature
        )
        return token

    def create_refresh_token(self, user: UserEntity) -> JwtEntity:
        payload_vo = JwtPayloadVo.create(
            sub=user.uid,
            email=user.email,
            typ=JwtTokenType.REFRESH,
            roles=list(user.roles),
            exp=expires_after(days=7),
        )
        payload_dto = JwtMapper.to_payload_dto_from_vo(payload_vo)
        jwt_dto: JwtDto = self._jwt_service.sign(payload_dto)
        token = JwtEntity.create_signed(
            payload=payload_vo, signature=jwt_dto.signature
        )
        return token

    def verify_token(self, token: str, subject: str | None = None) -> JwtEntity:
        token_dto: JwtDto = self._jwt_service.verify(token, subject)
        return JwtMapper.to_entity_from_jwt_dto(token_dto)

    def verify_refresh_token(self, token: str) -> JwtEntity:
        token_dto: JwtDto = self._jwt_service.verify_refresh_token(token)
        return JwtMapper.to_entity_from_jwt_dto(token_dto)
