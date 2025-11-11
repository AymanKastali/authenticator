from domain.services.jwt.revoke_jwt import RevokeJwt
from domain.services.jwt.validate_jwt import ValidateJwt
from domain.value_objects.jwt_payload import JwtPayloadVo


class LogoutUserUseCase:
    """Revoke an access token (logout)."""

    def __init__(self, validate_jwt: ValidateJwt, revoke_jwt: RevokeJwt):
        self._validate_jwt = validate_jwt
        self._revoke_jwt = revoke_jwt

    async def execute(self, token: str) -> None:
        payload_vo: JwtPayloadVo = self._validate_jwt.access(token)
        await self._revoke_jwt.revoke(payload_vo)
