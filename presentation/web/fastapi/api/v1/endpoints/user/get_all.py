from typing import Annotated

from fastapi import Depends, Query

from presentation.web.fastapi.api.v1.controllers.user.get_all import (
    GetAllUsersController,
)
from presentation.web.fastapi.dependencies.jwt import (
    get_current_authenticated_user,
)
from presentation.web.fastapi.dependencies.user import (
    get_user_all_users_controller_dependency,
)
from presentation.web.fastapi.schemas.response.auth.jwt.authenticated_user import (
    AuthenticatedUserResponseSchema,
)


async def get_all_users_endpoint(
    _authenticated_user: Annotated[
        AuthenticatedUserResponseSchema, Depends(get_current_authenticated_user)
    ],
    controller: Annotated[
        GetAllUsersController, Depends(get_user_all_users_controller_dependency)
    ],
    page: int = Query(default=1, ge=1, lt=1000),
    page_size: int = Query(default=20, ge=1, lt=50),
):
    return await controller.execute(page, page_size)
