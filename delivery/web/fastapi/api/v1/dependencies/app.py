from fastapi import Depends

from adapters.controllers.policy.list import ListPoliciesController
from application.services.policy import PolicyService
from delivery.web.fastapi.api.v1.handlers.app.list_policies import (
    ListPoliciesHandler,
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


# -----------------------------------------------------------------------------
# HANDLERS
# -----------------------------------------------------------------------------
def list_policies_handler_dependency(
    controller: ListPoliciesController = Depends(
        list_policies_controller_dependency
    ),
) -> ListPoliciesHandler:
    """Provide use case for registering a user"""
    return ListPoliciesHandler(controller)
