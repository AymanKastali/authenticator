from fastapi import Depends

from adapters.controllers.user_controllers.get_all_users_controller import (
    GetAllUsersController,
)
from adapters.controllers.user_controllers.get_user_by_id_controller import (
    GetUserByIdController,
)
from adapters.controllers.user_controllers.get_user_me_controller import (
    GetUserMeController,
)
from delivery.web.fastapi.api.v1.dependencies.user_dependencies.controller_dependencies import (
    get_get_all_users_controller,
    get_get_user_by_id_controller,
    get_get_user_me_controller,
)
from delivery.web.fastapi.api.v1.handlers.user_handlers.get_all_users_handler import (
    GetAllUsersHandler,
)
from delivery.web.fastapi.api.v1.handlers.user_handlers.get_user_by_id_handler import (
    GetUserByIdHandler,
)
from delivery.web.fastapi.api.v1.handlers.user_handlers.get_user_me_handler import (
    GetUserMeHandler,
)


def get_get_user_by_id_handler(
    controller: GetUserByIdController = Depends(get_get_user_by_id_controller),
) -> GetUserByIdHandler:
    return GetUserByIdHandler(controller)


def get_get_all_users_handler(
    controller: GetAllUsersController = Depends(get_get_all_users_controller),
) -> GetAllUsersHandler:
    return GetAllUsersHandler(controller)


def get_get_user_me_handler(
    controller: GetUserMeController = Depends(get_get_user_me_controller),
) -> GetUserMeHandler:
    return GetUserMeHandler(controller)
