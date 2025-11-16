from application.ports.repositories.jwt import JwtRedisRepositoryPort
from domain.value_objects.jwt_claims import JwtClaimsVo


class RevokeJwtUseCase:
    def __init__(self, jwt_redis_repo: JwtRedisRepositoryPort):
        self._jwt_redis_repo = jwt_redis_repo

    async def execute(self, claims: JwtClaimsVo) -> None:
        await self._jwt_redis_repo.blacklist_jwt(
            claims.jti.value, claims.exp.value.timestamp()
        )
