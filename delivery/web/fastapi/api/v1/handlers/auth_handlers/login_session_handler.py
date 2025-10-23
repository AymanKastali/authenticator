from fastapi import Response

from adapters.controllers.auth_controllers.login_session_controller import (
    SessionLoginController,
)
from adapters.presenters.request_models.login_user_model import LoginUserModel
from adapters.presenters.response_models.session_response_model import (
    SessionResponseModel,
)
from adapters.presenters.response_models.success_item_response_model import (
    ItemResponseModel,
)


class SessionLoginHandler:
    def __init__(self, controller: SessionLoginController):
        self._controller = controller

    async def execute(
        self, body: LoginUserModel, response: Response
    ) -> ItemResponseModel[SessionResponseModel]:
        session: SessionResponseModel = self._controller.execute(
            email=body.email, password=body.password
        )
        response.set_cookie(
            key="session_id",
            value=session.session_id,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        return ItemResponseModel[SessionResponseModel].build(
            data=session,
            status_code=200,
            message="Login successful",
        )
