from typing import Annotated

from fastapi import Depends, Request

from presentation.web.fastapi.api.v1.controllers.auth.jwt.logout import (
    JwtLogoutController,
)
from presentation.web.fastapi.api.v1.dependencies.controllers.jwt import (
    jwt_logout_controller_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.security.auth_helpers import (
    get_current_authenticated_user,
)
from presentation.web.fastapi.schemas.request.auth.jwt.logout import (
    LogoutJwtRequestSchema,
)
from presentation.web.fastapi.schemas.response.auth.jwt.authenticated_user import (
    AuthenticatedUserResponseSchema,
)


async def jwt_logout_endpoint(
    _request: Request,
    body: LogoutJwtRequestSchema,
    _authenticated_user: Annotated[
        AuthenticatedUserResponseSchema, Depends(get_current_authenticated_user)
    ],
    controller: Annotated[
        JwtLogoutController, Depends(jwt_logout_controller_dependency)
    ],
):
    return await controller.execute(body)
