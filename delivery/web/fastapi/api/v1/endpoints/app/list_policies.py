from fastapi import Depends

from adapters.dto.responses.auth.jwt.authenticated_user import (
    AuthenticatedUserOutDto,
)
from delivery.bootstrap.containers import app_container
from delivery.web.fastapi.api.v1.dependencies.jwt.auth import (
    get_current_authenticated_user,
)


async def list_policies_endpoint(
    _: AuthenticatedUserOutDto = Depends(get_current_authenticated_user),
    handler=Depends(lambda: app_container.list_policies_handler),
):
    return handler.execute()
