from uuid import UUID

from adapters.controllers.jwt.get_request_user_controller import (
    GetRequestUserController,
)
from adapters.dto.response_dto.user_response_models import (
    AuthenticatedUserResponseModel,
)


class GetRequestUserHandler:
    def __init__(self, controller: GetRequestUserController):
        self._controller = controller

    def execute(self, user_id: UUID) -> AuthenticatedUserResponseModel:
        return self._controller.execute(user_id)
