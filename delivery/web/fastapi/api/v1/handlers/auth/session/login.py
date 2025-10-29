from fastapi import Response

from adapters.controllers.auth.session.login import SessionLoginController
from adapters.dto.requests.auth.session.login import SessionLoginInDto
from adapters.dto.responses.auth.session.session import SessionOutDto
from adapters.dto.responses.generic.success.item import ItemOutDto


class SessionLoginHandler:
    def __init__(self, controller: SessionLoginController):
        self._controller = controller

    async def execute(
        self, body: SessionLoginInDto, response: Response
    ) -> ItemOutDto[SessionOutDto]:
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
        return ItemOutDto[SessionOutDto].build(
            data=session,
            status_code=200,
            message="Login successful",
        )
