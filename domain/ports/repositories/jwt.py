from abc import ABC, abstractmethod

from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.uuid_id import UUIDVo


class JwtRedisRepositoryPort(ABC):
    """Abstract port for managing JWT blacklist."""

    @abstractmethod
    async def blacklist_jwt(
        self, jti: UUIDVo, expire_at: DateTimeVo
    ) -> None: ...

    @abstractmethod
    async def is_jwt_blacklisted(self, jti: UUIDVo) -> bool: ...
