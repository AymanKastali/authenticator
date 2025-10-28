from fastapi import Depends, Request, Response

from adapters.dto.request_dto.session_request_dto import SessionLoginInDto
from delivery.bootstrap.containers.auth import session_auth_container
from delivery.web.fastapi.api.v1.handlers.auth.session.login import (
    SessionLoginHandler,
)


async def session_login_endpoint(
    _: Request,
    body: SessionLoginInDto,
    response: Response,
    handler: SessionLoginHandler = Depends(
        lambda: session_auth_container.session_login_handler
    ),
):
    return await handler.execute(body, response)
