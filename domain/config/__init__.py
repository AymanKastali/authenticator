from .config_models import JwtDomainConfig, PasswordDomainConfig
from .domain_config import DomainConfig

password_config = PasswordDomainConfig()
jwt_config = JwtDomainConfig()
domain_config = DomainConfig(
    password_config=password_config, jwt_config=jwt_config
)
