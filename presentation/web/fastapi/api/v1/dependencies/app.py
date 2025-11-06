from fastapi import Depends

from application.services.policy import PolicyService
from presentation.web.fastapi.api.v1.controllers.app.list_policies import (
    ListPoliciesController,
)


# -----------------------------------------------------------------------------
# SERVICES
# -----------------------------------------------------------------------------
def policy_service_dependency() -> PolicyService:
    return PolicyService()


# -----------------------------------------------------------------------------
# CONTROLLERS
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def list_policies_controller_dependency(
    service: PolicyService = Depends(policy_service_dependency),
) -> ListPoliciesController:
    return ListPoliciesController(service)
