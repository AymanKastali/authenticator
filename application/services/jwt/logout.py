from application.services.jwt.jwt_blacklist import JwtBlacklistService
from application.use_cases.jwt.validate_jwt import ValidateJwtUseCase
from domain.entities.jwt_token import JwtEntity


class JwtLogoutUserService:
    def __init__(
        self,
        validate_jwt: ValidateJwtUseCase,
        blacklist_service: JwtBlacklistService,
    ):
        self._validate_jwt = validate_jwt
        self._blacklist_service = blacklist_service

    async def execute(self, token: str) -> None:
        token_entity: JwtEntity = self._validate_jwt.execute(
            token=token, token_type="refresh"
        )
        token_id: str = token_entity.uid.value
        token_expiry: int = int(token_entity.claims.exp.value.timestamp())
        await self._blacklist_service.blacklist(
            jti=token_id, expires_at=token_expiry
        )
