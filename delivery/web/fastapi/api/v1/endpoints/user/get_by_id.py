from typing import Annotated
from uuid import UUID

from fastapi import Depends

from adapters.dto.responses.auth.jwt.authenticated_user import (
    AuthenticatedUserOutDto,
)
from delivery.web.fastapi.api.v1.dependencies.jwt import (
    get_current_authenticated_user,
)
from delivery.web.fastapi.api.v1.dependencies.user import (
    get_user_by_id_handler_dependency,
)


async def get_user_by_id_endpoint(
    _: Annotated[
        AuthenticatedUserOutDto, Depends(get_current_authenticated_user)
    ],
    user_id: UUID,
    handler=Depends(get_user_by_id_handler_dependency),
):
    return handler.execute(user_id)
