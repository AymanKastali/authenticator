from application.use_cases.jwt.revoke_jwt import RevokeJwtUseCase
from application.use_cases.jwt.validate_jwt import ValidateJwtUseCase
from domain.entities.jwt_token import JwtEntity


class JwtLogoutUserService:
    def __init__(
        self, validate_jwt: ValidateJwtUseCase, revoke_jwt: RevokeJwtUseCase
    ):
        self._validate_jwt = validate_jwt
        self._revoke_jwt = revoke_jwt

    async def execute(self, token: str) -> None:
        token_entity: JwtEntity = self._validate_jwt.validate_access_token(
            token
        )
        await self._revoke_jwt.execute(token_entity.claims)
