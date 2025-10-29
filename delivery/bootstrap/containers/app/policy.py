from adapters.controllers.policy.list import ListPoliciesController
from application.services.policy import PolicyService
from delivery.web.fastapi.api.v1.handlers.app.list_policies import (
    ListPoliciesHandler,
)


class AppContainer:
    """Container for jwt-based authentication"""

    def __init__(self):
        # Services
        self.policy_service = PolicyService()

        # Controllers
        self.list_policies_controller = ListPoliciesController(
            service=self.policy_service
        )

        # Handlers
        self.list_policies_handler = ListPoliciesHandler(
            controller=self.list_policies_controller
        )
