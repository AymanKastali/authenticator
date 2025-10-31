from abc import ABC, abstractmethod
from datetime import datetime


class JwtRepositoryPort(ABC):
    @abstractmethod
    def add_token(self, jti: str, expires_at: datetime) -> None: ...

    @abstractmethod
    def is_token_blacklisted(self, jti: str) -> bool: ...

    @abstractmethod
    def get_revoked_tokens(self) -> set[str]: ...
