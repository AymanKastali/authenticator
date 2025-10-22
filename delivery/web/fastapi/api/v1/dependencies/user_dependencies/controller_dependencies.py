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
from application.use_cases.user_use_cases.get_all_users_uc import (
    GetAllUsersUseCase,
)
from application.use_cases.user_use_cases.get_user_by_id_uc import (
    GetUserByIdUseCase,
)
from application.use_cases.user_use_cases.get_user_me_uc import GetUserMeUseCase
from delivery.web.fastapi.api.v1.dependencies.user_dependencies.use_case_dependencies import (
    get_get_all_users_uc,
    get_get_user_by_id_uc,
    get_get_user_me_uc,
)


def get_get_user_by_id_controller(
    use_case: GetUserByIdUseCase = Depends(get_get_user_by_id_uc),
) -> GetUserByIdController:
    return GetUserByIdController(use_case)


def get_get_all_users_controller(
    use_case: GetAllUsersUseCase = Depends(get_get_all_users_uc),
) -> GetAllUsersController:
    return GetAllUsersController(use_case)


def get_get_user_me_controller(
    use_case: GetUserMeUseCase = Depends(get_get_user_me_uc),
) -> GetUserMeController:
    return GetUserMeController(use_case)
