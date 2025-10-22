from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request

from adapters.presenters.response_models.user_response_models import (
    AuthenticatedUserResponseModel,
)
from delivery.web.fastapi.api.v1.dependencies.jwt.jwt_dependencies import (
    get_current_user,
)
from delivery.web.fastapi.api.v1.dependencies.user_dependencies.handler_dependencies import (
    get_get_all_users_handler,
    get_get_user_by_id_handler,
    get_get_user_me_handler,
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


async def get_me_endpoint(
    _: Request,
    current_user: Annotated[
        AuthenticatedUserResponseModel, Depends(get_current_user)
    ],
    handler: GetUserMeHandler = Depends(get_get_user_me_handler),
):
    return handler.execute(user_id=UUID(current_user.uid))


async def get_user_by_id_endpoint(
    _: Request,
    user_id: UUID,
    handler: GetUserByIdHandler = Depends(get_get_user_by_id_handler),
):
    return handler.execute(user_id)


async def get_all_users_endpoint(
    _: Request, handler: GetAllUsersHandler = Depends(get_get_all_users_handler)
):
    return handler.execute()
