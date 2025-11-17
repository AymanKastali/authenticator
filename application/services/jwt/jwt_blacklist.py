from domain.exceptions.domain_errors import JwtRevokedError
from domain.ports.repositories.jwt import JwtBlacklistRepositoryPort


class JwtBlacklistService:
    """Application service to check or blacklist JWTs according to domain rules."""

    def __init__(self, repository: JwtBlacklistRepositoryPort):
        self._repository = repository

    async def blacklist(self, jti: str, expires_at: int) -> None:
        """Blacklist a JWT."""
        await self._repository.add(jti, expires_at)

    async def assert_not_blacklisted(self, jti: str) -> None:
        """Raise if JWT is blacklisted."""
        if await self._repository.contains(jti):
            raise JwtRevokedError()
