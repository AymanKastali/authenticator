from typing import Annotated

from fastapi import Depends, Request

from presentation.web.fastapi.api.v1.controllers.auth.jwt.refresh_token import (
    RefreshJwtTokenController,
)
from presentation.web.fastapi.api.v1.dependencies.jwt import (
    jwt_refresh_token_controller_dependency,
)
from presentation.web.fastapi.schemas.request.auth.jwt.refresh_token import (
    RefreshJwtTokenRequestSchema,
)


async def refresh_jwt_token_endpoint(
    _request: Request,
    body: RefreshJwtTokenRequestSchema,
    controller: Annotated[
        RefreshJwtTokenController,
        Depends(jwt_refresh_token_controller_dependency),
    ],
):
    return await controller.execute(body)
