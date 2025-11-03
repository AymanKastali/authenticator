from fastapi import Depends, Request

from adapters.dto.requests.auth.registration.login import LoginUserInDto
from delivery.web.fastapi.api.v1.dependencies.registration import (
    register_user_handler_dependency,
)
from delivery.web.fastapi.api.v1.handlers.auth.registration.register import (
    RegisterUserHandler,
)


async def register_user_endpoint(
    _: Request,
    body: LoginUserInDto,
    handler: RegisterUserHandler = Depends(register_user_handler_dependency),
):
    return await handler.execute(body)
