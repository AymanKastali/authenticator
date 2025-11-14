from domain.entities.jwt_token import JwtEntity
from domain.services.auth.jwt.revoke_jwt import RevokeJwt
from domain.services.auth.jwt.validate_jwt import ValidateJwt


class LogoutUserUseCase:
    def __init__(self, validate_jwt: ValidateJwt, revoke_jwt: RevokeJwt):
        self._validate_jwt = validate_jwt
        self._revoke_jwt = revoke_jwt

    async def execute(self, token: str) -> None:
        token_entity: JwtEntity = self._validate_jwt.validate_access_token(
            token
        )
        await self._revoke_jwt.execute(token_entity.claims)
