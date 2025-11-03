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


async def list_policies_endpoint(
    _: AuthenticatedUserOutDto = Depends(get_current_authenticated_user),
    handler=Depends(list_policies_handler_dependency),
):
    return handler.execute()
