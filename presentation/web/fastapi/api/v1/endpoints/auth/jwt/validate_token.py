from typing import Annotated

from fastapi import Depends, Request

from presentation.web.fastapi.api.v1.controllers.auth.jwt.validate_token import (
    ValidateJwtTokenController,
)
from presentation.web.fastapi.dependencies.jwt import (
    jwt_validate_token_controller_dependency,
)
from presentation.web.fastapi.schemas.request.auth.jwt.validate_token import (
    ValidateJwtTokenRequestSchema,
)


async def validate_jwt_token_endpoint(
    _request: Request,
    body: ValidateJwtTokenRequestSchema,
    controller: Annotated[
        ValidateJwtTokenController,
        Depends(jwt_validate_token_controller_dependency),
    ],
):
    return await controller.execute(body)
