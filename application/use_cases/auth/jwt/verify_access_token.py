from application.dto.auth.jwt.payload import JwtPayloadDto
from application.mappers.jwt import JwtMapper
from domain.services.jwt.revoke_jwt import RevokeJwt
from domain.services.jwt.validate_jwt import ValidateJwt
from domain.value_objects.jwt_payload import JwtPayloadVo


class VerifyAccessTokenUseCase:
    """Verify access token and ensure it is not revoked."""

    def __init__(self, validate_jwt: ValidateJwt, revoke_jwt: RevokeJwt):
        self._validate_jwt = validate_jwt
        self._revoke_jwt = revoke_jwt

    async def execute(
        self, token: str, subject: str | None = None
    ) -> JwtPayloadDto:
        payload_vo: JwtPayloadVo = self._validate_jwt.access(token, subject)
        await self._revoke_jwt.assert_not_revoked(payload_vo.jti)
        return JwtMapper.to_payload_dto_from_vo(payload_vo)
