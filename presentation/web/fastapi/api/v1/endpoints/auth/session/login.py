from typing import Annotated

from fastapi import Depends, Request, Response

from presentation.web.fastapi.api.v1.controllers.auth.session.login import (
    SessionLoginController,
)
from presentation.web.fastapi.api.v1.dependencies.session import (
    session_auth_controller_dependency,
)
from presentation.web.fastapi.schemas.request.auth.session.login import (
    SessionLoginRequestSchema,
)


async def session_login_endpoint(
    _: Request,
    body: SessionLoginRequestSchema,
    response: Response,
    controller: Annotated[
        SessionLoginController, Depends(session_auth_controller_dependency)
    ],
):
    return await controller.execute(body, response)
