from typing import Annotated

from fastapi import Depends, Request

from presentation.web.fastapi.api.v1.controllers.auth.jwt.verify_token import (
    VerifyJwtTokenController,
)
from presentation.web.fastapi.api.v1.dependencies.jwt import (
    jwt_verify_access_token_controller_dependency,
)
from presentation.web.fastapi.schemas.request.auth.jwt.verify_token import (
    VerifyJwtTokenRequestSchema,
)


async def verify_jwt_access_token_endpoint(
    _request: Request,
    body: VerifyJwtTokenRequestSchema,
    controller: Annotated[
        VerifyJwtTokenController,
        Depends(jwt_verify_access_token_controller_dependency),
    ],
):
    return await controller.execute(body)
