from typing import Annotated

from fastapi import Depends

from presentation.web.fastapi.api.v1.controllers.app.list_policies import (
    ListPoliciesController,
)
from presentation.web.fastapi.api.v1.dependencies.controllers.policy import (
    list_policies_controller_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.security.auth_helpers import (
    get_current_authenticated_user,
)
from presentation.web.fastapi.schemas.response.auth.jwt.authenticated_user import (
    AuthenticatedUserResponseSchema,
)


def list_policies_endpoint(
    _authenticated_user: Annotated[
        AuthenticatedUserResponseSchema, Depends(get_current_authenticated_user)
    ],
    controller: Annotated[
        ListPoliciesController, Depends(list_policies_controller_dependency)
    ],
):
    return controller.execute()
