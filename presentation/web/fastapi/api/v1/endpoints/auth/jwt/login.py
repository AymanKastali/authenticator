from fastapi import Depends, Request
from typing_extensions import Annotated

from presentation.web.fastapi.api.v1.controllers.auth.jwt.login import (
    JwtLoginController,
)
from presentation.web.fastapi.api.v1.dependencies.controllers.jwt import (
    jwt_login_controller_dependency,
)
from presentation.web.fastapi.schemas.request.auth.registration.login import (
    LoginUserRequestSchema,
)


async def jwt_login_endpoint(
    _request: Request,
    body: LoginUserRequestSchema,
    controller: Annotated[
        JwtLoginController, Depends(jwt_login_controller_dependency)
    ],
):
    return await controller.execute(body)
