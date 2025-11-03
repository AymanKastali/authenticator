from typing import Annotated

from fastapi import Depends

from adapters.dto.responses.auth.jwt.authenticated_user import (
    AuthenticatedUserOutDto,
)
from delivery.web.fastapi.api.v1.dependencies.app import (
    list_policies_handler_dependency,
)
from delivery.web.fastapi.api.v1.dependencies.jwt import (
    get_current_authenticated_user,
)
from delivery.web.fastapi.api.v1.handlers.app.list_policies import (
    ListPoliciesHandler,
)


def list_policies_endpoint(
    _authenticated_user: Annotated[
        AuthenticatedUserOutDto, Depends(get_current_authenticated_user)
    ],
    handler: Annotated[
        ListPoliciesHandler, Depends(list_policies_handler_dependency)
    ],
):
    return handler.execute()
