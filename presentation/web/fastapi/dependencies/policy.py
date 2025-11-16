from fastapi import Depends

from application.use_cases.list_policies import ListPoliciesUseCase
from domain.factories.jwt_policy import JwtPolicyBuilder
from domain.factories.password_policy import PasswordPolicyBuilder
from domain.interfaces.policy import PolicyInterface
from presentation.web.fastapi.api.v1.controllers.app.list_policies import (
    ListPoliciesController,
)


# Domain
def password_policies() -> list[PolicyInterface]:
    return (
        PasswordPolicyBuilder()
        .add_length_policy(min_length=8, max_length=128)
        .add_complexity_policy(
            require_upper=True,
            require_lower=True,
            require_digit=True,
            require_special=True,
        )
        .build()
    )


def jwt_policies() -> list[PolicyInterface]:
    return (
        JwtPolicyBuilder()
        .add_expiry_policy(
            access_token_max_age_seconds=1 * 60 * 60 * 24 * 7,  # 7 days
            refresh_token_max_age_seconds=1 * 60 * 60 * 24 * 30,  # 30 days
        )
        .build()
    )


# Application
def list_policies_uc_dependency() -> ListPoliciesUseCase:
    policies = jwt_policies() + password_policies()
    return ListPoliciesUseCase(policies)


# Presentation
def list_policies_controller_dependency(
    service: ListPoliciesUseCase = Depends(list_policies_uc_dependency),
) -> ListPoliciesController:
    return ListPoliciesController(service)
