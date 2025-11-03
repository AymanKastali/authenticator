from fastapi import Depends, Query

from adapters.dto.responses.auth.jwt.authenticated_user import (
    AuthenticatedUserOutDto,
)
from delivery.web.fastapi.api.v1.dependencies.jwt import (
    get_current_authenticated_user,
)
from delivery.web.fastapi.api.v1.dependencies.user import (
    get_user_all_users_handler_dependency,
)


async def get_all_users_endpoint(
    _: AuthenticatedUserOutDto = Depends(get_current_authenticated_user),
    page: int = Query(default=1, ge=1, lt=1000),
    page_size: int = Query(default=20, ge=1, lt=50),
    handler=Depends(get_user_all_users_handler_dependency),
):
    return handler.execute(page, page_size)
