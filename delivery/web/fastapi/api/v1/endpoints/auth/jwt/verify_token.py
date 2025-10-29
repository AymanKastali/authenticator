from fastapi import Depends, Request

from adapters.dto.requests.auth.jwt.verify_token import VerifyJwtTokenInDto
from delivery.bootstrap.containers.auth import jwt_auth_container
from delivery.web.fastapi.api.v1.handlers.auth.jwt.verify_token import (
    VerifyJwtTokenHandler,
)


async def verify_jwt_token_endpoint(
    _: Request,
    body: VerifyJwtTokenInDto,
    handler: VerifyJwtTokenHandler = Depends(
        lambda: jwt_auth_container.verify_jwt_token_handler
    ),
):
    return await handler.execute(body)
