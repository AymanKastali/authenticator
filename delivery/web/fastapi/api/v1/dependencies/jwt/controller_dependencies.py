from fastapi import Depends

from adapters.controllers.jwt.get_request_user_controller import (
    GetRequestUserController,
)
from application.use_cases.user_use_cases.get_request_user_uc import (
    GetRequestUserUseCase,
)
from delivery.web.fastapi.api.v1.dependencies.jwt.use_case_dependencies import (
    get_request_user_use_case,
)


def get_request_user_controller(
    use_case: GetRequestUserUseCase = Depends(get_request_user_use_case),
) -> GetRequestUserController:
    return GetRequestUserController(use_case)
