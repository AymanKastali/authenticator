from .config_models import PasswordConfig
from .domain_config import DomainConfig

password_config = PasswordConfig()
domain_config = DomainConfig(password_config=password_config)
