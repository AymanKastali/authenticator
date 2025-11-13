from domain.exceptions.domain_errors import JwtRevokedError
from domain.ports.repositories.jwt import JwtRedisRepositoryPort
from domain.value_objects.identifiers import UUIDVo
from domain.value_objects.jwt_claims import JwtClaimsVo


class RevokeJwt:
    """Revoke (blacklist) JWTs and check revocation status."""

    def __init__(self, jwt_redis_repo: JwtRedisRepositoryPort):
        self._jwt_redis_repo = jwt_redis_repo

    async def revoke(self, claims: JwtClaimsVo) -> None:
        await self._jwt_redis_repo.blacklist_jwt(claims.jti, claims.exp)

    async def assert_not_revoked(self, jti: UUIDVo) -> None:
        if await self._jwt_redis_repo.is_jwt_blacklisted(jti):
            raise JwtRevokedError()
