from fastapi import HTTPException, Response

from application.services.auth.session import SessionAuthService
from presentation.web.fastapi.schemas.request.auth.session.login import (
    SessionLoginRequestSchema,
)
from presentation.web.fastapi.schemas.response.auth.session.session import (
    SessionResponseSchema,
)
from presentation.web.fastapi.schemas.response.generic.success.item import (
    ItemResponseSchema,
)


class SessionLoginController:
    def __init__(self, service: SessionAuthService):
        self._service = service

    async def execute(
        self, body: SessionLoginRequestSchema, response: Response
    ) -> ItemResponseSchema[SessionResponseSchema]:
        session_id: str | None = await self._service.create_session(
            email=body.email, password=body.password
        )
        if not session_id:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        session = SessionResponseSchema(
            session_id=session_id, user_id="user_id"
        )

        response.set_cookie(
            key="session_id",
            value=session.session_id,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        return ItemResponseSchema[SessionResponseSchema].build(
            data=session,
            status_code=200,
            message="Login successful",
        )
