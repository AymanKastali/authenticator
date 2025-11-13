from application.dto.auth.jwt.claims import JwtClaimsDto
from application.mappers.jwt import JwtMapper
from domain.entities.auth.jwt.token import JwtEntity
from domain.services.jwt.validate_jwt import ValidateJwt


class VerifyRefreshTokenUseCase:
    def __init__(self, validate_jwt: ValidateJwt):
        self._validate_jwt = validate_jwt

    async def execute(self, token: str) -> JwtClaimsDto:
        token_entity: JwtEntity = self._validate_jwt.validate_refresh_token(
            token
        )
        return JwtMapper.to_claims_dto_from_vo(token_entity.claims)
