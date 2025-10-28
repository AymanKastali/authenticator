from fastapi import Depends, Request, Response

from adapters.dto.request_dto.login_user_model import LoginUserModel
from delivery.bootstrap.containers.auth import session_auth_container
from delivery.web.fastapi.api.v1.handlers.auth_handlers.login_session_handler import (
    SessionLoginHandler,
)


async def session_login_endpoint(
    _: Request,
    request_body: LoginUserModel,
    response: Response,
    handler: SessionLoginHandler = Depends(
        lambda: session_auth_container.session_login_handler
    ),
):
    return await handler.execute(request_body, response)
