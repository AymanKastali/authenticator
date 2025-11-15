from application.dto.auth.jwt.claims import JwtClaimsDto
from application.mappers.jwt import JwtMapper
from domain.entities.jwt_token import JwtEntity
from domain.services.auth.jwt.assert_jwt_revocation import AssertJwtRevocation
from domain.services.auth.jwt.validate_jwt import ValidateJwt
from domain.value_objects.uuid_id import UUIDVo


class ValidateAccessTokenUseCase:
    def __init__(
        self,
        validate_jwt: ValidateJwt,
        assert_jwt_revocation: AssertJwtRevocation,
    ):
        self._validate_jwt = validate_jwt
        self._assert_jwt_revocation = assert_jwt_revocation

    async def execute(
        self, token: str, subject: str | None = None
    ) -> JwtClaimsDto:
        subject_vo = UUIDVo.from_string(subject) if subject else None
        token_entity: JwtEntity = self._validate_jwt.validate_access_token(
            token, subject_vo
        )
        await self._assert_jwt_revocation.execute(token_entity.uid)
        return JwtMapper.to_claims_dto_from_vo(token_entity.claims)
