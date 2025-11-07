from typing import Annotated

from fastapi import Depends, Request

from presentation.web.fastapi.api.v1.controllers.auth.registration.register import (
    RegisterUserController,
)
from presentation.web.fastapi.api.v1.dependencies.controllers.auth import (
    register_user_controller_dependency,
)
from presentation.web.fastapi.schemas.request.auth.registration.login import (
    LoginUserRequestSchema,
)


async def register_user_endpoint(
    _: Request,
    body: LoginUserRequestSchema,
    controller: Annotated[
        RegisterUserController, Depends(register_user_controller_dependency)
    ],
):
    return await controller.execute(body)
