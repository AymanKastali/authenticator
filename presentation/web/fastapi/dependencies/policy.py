from fastapi import Depends

from application.use_cases.list_policies import ListPoliciesUseCase
from domain.factories.jwt_policy import JwtPolicyBuilder
from domain.factories.password_policy import PasswordPolicyBuilder
from domain.interfaces.policy import PolicyInterface
from presentation.web.fastapi.api.v1.controllers.app.list_policies import (
    ListPoliciesController,
)
from presentation.web.fastapi.dependencies.config import (
    jwt_domain_config_dependency,
    password_domain_config_dependency,
)


# Domain
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


# Application
def list_policies_uc_dependency() -> ListPoliciesUseCase:
    policies = jwt_policies() + password_policies()
    return ListPoliciesUseCase(policies)


# Presentation
def list_policies_controller_dependency(
    service: ListPoliciesUseCase = Depends(list_policies_uc_dependency),
) -> ListPoliciesController:
    return ListPoliciesController(service)
