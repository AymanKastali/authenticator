from application.dto.auth.jwt.claims import JwtClaimsDto
from application.mappers.jwt import JwtMapper
from application.use_cases.jwt.validate_jwt import ValidateJwtUseCase
from domain.entities.jwt_token import JwtEntity


class ValidateJwtRefreshTokenService:
    def __init__(self, validate_jwt: ValidateJwtUseCase):
        self._validate_jwt = validate_jwt

    async def execute(self, token: str) -> JwtClaimsDto:
        token_entity: JwtEntity = self._validate_jwt.validate_refresh_token(
            token
        )
        return JwtMapper.to_claims_dto_from_vo(token_entity.claims)
