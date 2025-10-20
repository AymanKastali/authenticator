from fastapi import Response

from adapters.controllers.login_session_controller import SessionLoginController
from adapters.presenters.request_models.login_user_model import LoginUserModel
from adapters.presenters.response_models.success_item_response_model import (
    ItemResponseModel,
)


class SessionLoginHandler:
    def __init__(self, controller: SessionLoginController):
        self._controller = controller

    async def execute(
        self, body: LoginUserModel, response: Response
    ) -> ItemResponseModel[dict]:
        session_id: str = self._controller.execute(
            email_address=body.email_address, password=body.password
        )
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        print("xxxxxxx", response.headers)
        return ItemResponseModel[dict].build(
            data={"session_id": session_id},
            status_code=200,
            message="Login successful",
        )
