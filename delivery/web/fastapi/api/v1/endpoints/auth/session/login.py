from fastapi import Depends, Request, Response

from adapters.dto.requests.auth.session.login import SessionLoginInDto
from delivery.web.fastapi.api.v1.dependencies.session import (
    session_auth_handler_dependency,
)
from delivery.web.fastapi.api.v1.handlers.auth.session.login import (
    SessionLoginHandler,
)


async def session_login_endpoint(
    _: Request,
    body: SessionLoginInDto,
    response: Response,
    handler: SessionLoginHandler = Depends(session_auth_handler_dependency),
):
    return await handler.execute(body, response)
