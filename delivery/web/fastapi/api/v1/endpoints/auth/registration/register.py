from fastapi import Depends, Request

from adapters.dto.request_dto.login_user_model import LoginUserModel
from delivery.bootstrap.containers.auth import registration_container
from delivery.web.fastapi.api.v1.handlers.auth.registration.register import (
    RegisterUserHandler,
)


async def register_user_endpoint(
    _: Request,
    body: LoginUserModel,
    handler: RegisterUserHandler = Depends(
        lambda: registration_container.register_user_handler
    ),
):
    return await handler.execute(body)
