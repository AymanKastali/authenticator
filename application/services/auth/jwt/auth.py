from application.dto.auth.jwt.payload import JwtPayloadDto
from application.dto.auth.jwt.tokens import JwtTokensDto
from application.mappers.jwt import JwtMapper
from application.services.auth.authentication import AuthService
from domain.entities.user import UserEntity
from domain.services.jwt import JwtDomainService
from domain.value_objects.email import EmailVo
from domain.value_objects.identifiers import UUIDVo
from domain.value_objects.jwt_payload import JwtPayloadVo


class JwtAuthService:
    """Responsible for signing and verifying JWTs."""

    def __init__(
        self, auth_service: AuthService, jwt_service: JwtDomainService
    ):
        self._auth_service = auth_service
        self._jwt_service = jwt_service

    def _create_user_tokens(self, user: UserEntity) -> JwtTokensDto:
        access_token: str = self._jwt_service.create_access_token(user)
        refresh_token: str = self._jwt_service.create_refresh_token(user)
        return JwtTokensDto(
            access_token=access_token, refresh_token=refresh_token
        )

    async def login(self, email: str, password: str) -> JwtTokensDto:
        email_vo = EmailVo.from_string(email)
        user: UserEntity = await self._auth_service.authenticate_user(
            email_vo, password
        )
        if user.deleted:
            raise ValueError("Deleted")
        return self._create_user_tokens(user)

    async def logout(self, token: str) -> None:
        payload_vo: JwtPayloadVo = self._jwt_service.verify_token(token)
        await self._jwt_service.blacklist_token(payload_vo)

    def verify_jwt_token(
        self, token: str, subject: str | None = None
    ) -> JwtPayloadDto:
        payload_vo: JwtPayloadVo = self._jwt_service.verify_token(
            token, subject
        )
        return JwtMapper.to_payload_dto_from_vo(payload_vo)

    def verify_refresh_token(self, token: str) -> JwtPayloadDto:
        payload_vo: JwtPayloadVo = self._jwt_service.verify_refresh_token(token)
        return JwtMapper.to_payload_dto_from_vo(payload_vo)

    async def refresh_jwt_token(self, refresh_token: str) -> JwtTokensDto:
        payload_vo: JwtPayloadVo = self._jwt_service.verify_refresh_token(
            refresh_token
        )
        user: UserEntity = await self._auth_service.get_user_by_id(
            user_id=payload_vo.sub
        )
        return self._create_user_tokens(user)

    async def is_jwt_blacklisted(self, jti: str) -> bool:
        return await self._jwt_service.is_jwt_blacklisted(
            UUIDVo.from_string(jti)
        )
