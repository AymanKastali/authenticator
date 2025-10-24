import os

from adapters.config.adapters_config import AdaptersConfig
from adapters.config.jwt_config import JwtConfig


class AdaptersConfigFactory:
    """
    Factory for creating DomainConfig instances from environment variables or defaults.
    Supports modular methods for different concerns.
    """

    @staticmethod
    def load_jwt_config() -> JwtConfig:
        return JwtConfig(
            secret_key=os.getenv("JWT_SECRET_KEY", "supersecret"),
            algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            issuer=os.getenv("JWT_ISSUER", "auth.myapp.com"),
            audience=os.getenv("JWT_AUDIENCE", "api.myapp.com"),
            leeway=int(os.getenv("JWT_LEEWAY", "0")),
        )

    @classmethod
    def load(cls) -> AdaptersConfig:
        """
        Build the full DomainConfig by combining all specialized configs.
        """
        jwt_cfg = cls.load_jwt_config()
        return AdaptersConfig(jwt=jwt_cfg)
