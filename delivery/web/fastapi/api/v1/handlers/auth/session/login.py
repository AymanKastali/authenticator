from fastapi import Response

from adapters.controllers.auth.session.login import (
    SessionLoginController,
)
from adapters.dto.request_dto.session_request_dto import SessionLoginInDto
from adapters.dto.response_dto.session_response_dto import SessionOutDto
from adapters.dto.response_dto.success_item_response_model import (
    ItemResponseModel,
)


class SessionLoginHandler:
    def __init__(self, controller: SessionLoginController):
        self._controller = controller

    async def execute(
        self, body: SessionLoginInDto, response: Response
    ) -> ItemResponseModel[SessionOutDto]:
        session: SessionOutDto = self._controller.execute(
            email=body.email, password=body.password
        )
        response.set_cookie(
            key="session_id",
            value=session.session_id,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        return ItemResponseModel[SessionOutDto].build(
            data=session,
            status_code=200,
            message="Login successful",
        )
