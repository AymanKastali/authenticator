from .app import AppConfig


def get_app_config() -> AppConfig:
    """Return a singleton AppConfig instance."""
    return AppConfig()
