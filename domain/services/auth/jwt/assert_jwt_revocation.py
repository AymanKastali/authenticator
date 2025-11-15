from domain.exceptions.domain_errors import JwtRevokedError
from domain.ports.repositories.jwt import JwtRedisRepositoryPort
from domain.value_objects.uuid_id import UUIDVo


class AssertJwtRevocation:
    def __init__(self, jwt_redis_repo: JwtRedisRepositoryPort):
        self._jwt_redis_repo = jwt_redis_repo

    async def execute(self, jti: UUIDVo) -> None:
        if await self._jwt_redis_repo.is_jwt_blacklisted(jti):
            raise JwtRevokedError()
