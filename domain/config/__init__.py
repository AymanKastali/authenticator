from .config_models import JwtConfig, PasswordConfig
from .domain_config import DomainConfig

password_config = PasswordConfig()
jwt_config = JwtConfig()
domain_config = DomainConfig(
    password_config=password_config, jwt_config=jwt_config
)
