import os

from domain.config.config_models import JwtConfig, LoginConfig, PasswordConfig
from domain.config.domain_config import DomainConfig


class DomainConfigFactory:
    """
    Factory for creating DomainConfig instances from environment variables or defaults.
    Supports modular methods for different concerns.
    """

    @staticmethod
    def load_password_config() -> PasswordConfig:
        return PasswordConfig(
            min_length=int(os.getenv("MIN_PASSWORD_LENGTH", "8")),
            max_length=int(os.getenv("MAX_PASSWORD_LENGTH", "128")),
        )

    @staticmethod
    def load_jwt_config() -> JwtConfig:
        return JwtConfig(
            access_token_expiration_minutes=int(
                os.getenv("JWT_ACCESS_TOKEN_EXPIRATION_MINUTES", "60")
            ),
            refresh_token_expiration_days=int(
                os.getenv("JWT_REFRESH_TOKEN_EXPIRATION_DAYS", "7")
            ),
            secret_key=os.getenv("JWT_SECRET_KEY", "supersecret"),
            algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            issuer=os.getenv("JWT_ISSUER", "auth.myapp.com"),
            audience=os.getenv("JWT_AUDIENCE", "api.myapp.com"),
            leeway_seconds=int(os.getenv("JWT_LEEWAY_SECONDS", "0")),
        )

    @staticmethod
    def load_login_config() -> LoginConfig:
        return LoginConfig(
            max_login_attempts=int(os.getenv("MAX_LOGIN_ATTEMPTS", "5")),
            enable_two_factor_auth=bool(int(os.getenv("ENABLE_2FA", "1"))),
            password_expiration_days=int(
                os.getenv("PASSWORD_EXPIRATION_DAYS", "90")
            ),
        )

    @classmethod
    def load(cls) -> DomainConfig:
        """
        Build the full DomainConfig by combining all specialized configs.
        """
        password_cfg = cls.load_password_config()
        jwt_cfg = cls.load_jwt_config()
        login_cfg = cls.load_login_config()
        return DomainConfig(password=password_cfg, jwt=jwt_cfg, login=login_cfg)
