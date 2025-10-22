from fastapi import Depends

from adapters.controllers.jwt.get_request_user_controller import (
    GetRequestUserController,
)
from delivery.web.fastapi.api.v1.dependencies.jwt.controller_dependencies import (
    get_request_user_controller,
)
from delivery.web.fastapi.api.v1.handlers.jwt.get_user_me_handler import (
    GetRequestUserHandler,
)


def get_get_user_me_handler(
    controller: GetRequestUserController = Depends(get_request_user_controller),
) -> GetRequestUserHandler:
    return GetRequestUserHandler(controller)
