from application.dto.auth.jwt.payload import JwtPayloadDto
from application.mappers.jwt import JwtMapper
from domain.services.jwt.validate_jwt import ValidateJwt
from domain.value_objects.jwt_payload import JwtPayloadVo


class VerifyRefreshTokenUseCase:
    """Verify refresh token validity."""

    def __init__(self, validate_jwt: ValidateJwt):
        self._validate_jwt = validate_jwt

    async def execute(self, token: str) -> JwtPayloadDto:
        payload_vo: JwtPayloadVo = self._validate_jwt.refresh(token)
        return JwtMapper.to_payload_dto_from_vo(payload_vo)
