from abc import ABC, abstractmethod


class OAuthServicePort(ABC):
    @abstractmethod
    def authenticate_provider(self, provider: str, code: str) -> dict: ...
