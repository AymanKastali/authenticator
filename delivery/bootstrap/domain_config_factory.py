import os

from domain.config.config_models import LoginConfig, PasswordConfig
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
        login_cfg = cls.load_login_config()
        return DomainConfig(password=password_cfg, login=login_cfg)
