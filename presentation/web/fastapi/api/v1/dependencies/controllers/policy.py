from fastapi import Depends

from application.services.policy import PolicyService
from presentation.web.fastapi.api.v1.controllers.app.list_policies import (
    ListPoliciesController,
)
from presentation.web.fastapi.api.v1.dependencies.application.policy import (
    policy_service_dependency,
)


def list_policies_controller_dependency(
    service: PolicyService = Depends(policy_service_dependency),
) -> ListPoliciesController:
    return ListPoliciesController(service)
