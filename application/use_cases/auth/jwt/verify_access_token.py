from application.dto.auth.jwt.claims import JwtClaimsDto
from application.mappers.jwt import JwtMapper
from domain.entities.auth.jwt.token import JwtEntity
from domain.services.jwt.revoke_jwt import RevokeJwt
from domain.services.jwt.validate_jwt import ValidateJwt
from domain.value_objects.identifiers import UUIDVo


class VerifyAccessTokenUseCase:
    def __init__(self, validate_jwt: ValidateJwt, revoke_jwt: RevokeJwt):
        self._validate_jwt = validate_jwt
        self._revoke_jwt = revoke_jwt

    async def execute(
        self, token: str, subject: str | None = None
    ) -> JwtClaimsDto:
        subject_vo = UUIDVo.from_string(subject) if subject else None
        token_entity: JwtEntity = self._validate_jwt.validate_access_token(
            token, subject_vo
        )
        await self._revoke_jwt.assert_not_revoked(token_entity.uid)
        return JwtMapper.to_claims_dto_from_vo(token_entity.claims)
