from typing import Annotated
from uuid import UUID

from fastapi import Depends

from presentation.web.fastapi.api.v1.controllers.user.get_by_id import (
    GetUserByIdController,
)
from presentation.web.fastapi.api.v1.dependencies.controllers.user import (
    get_user_by_id_controller_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.security.auth_helpers import (
    get_current_authenticated_user,
)
from presentation.web.fastapi.schemas.response.auth.jwt.authenticated_user import (
    AuthenticatedUserResponseSchema,
)


async def get_user_by_id_endpoint(
    _authenticated_user: Annotated[
        AuthenticatedUserResponseSchema, Depends(get_current_authenticated_user)
    ],
    user_id: UUID,
    controller: Annotated[
        GetUserByIdController, Depends(get_user_by_id_controller_dependency)
    ],
):
    return await controller.execute(user_id)
