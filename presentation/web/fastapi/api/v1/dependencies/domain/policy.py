from domain.factories.jwt_policy import JwtPolicyBuilder
from domain.factories.password_policy import PasswordPolicyBuilder
from domain.interfaces.policy import PolicyInterface
from presentation.web.fastapi.api.v1.dependencies.domain.config import (
    jwt_domain_config_dependency,
    password_domain_config_dependency,
)


def password_policies() -> list[PolicyInterface]:
    config = password_domain_config_dependency()
    return (
        PasswordPolicyBuilder(config)
        .add_length_policy()
        .add_complexity_policy()
        .build()
    )


def jwt_policies() -> list[PolicyInterface]:
    config = jwt_domain_config_dependency()
    return JwtPolicyBuilder(config).add_expiry_policy().build()
