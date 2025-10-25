from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request

from adapters.dto.response_dto.user_response_models import (
    AuthenticatedUserResponseModel,
)
from delivery.bootstrap.containers import (
    feature_user_container as user_container,
)
from delivery.web.fastapi.api.v1.dependencies.jwt_dependencies import (
    get_current_user,
)


async def get_me_endpoint(
    _: Request,
    current_user: Annotated[
        AuthenticatedUserResponseModel, Depends(get_current_user)
    ],
    handler=Depends(lambda: user_container.get_user_me_handler),
):
    return handler.execute(user_id=current_user.as_uuid())


async def get_user_by_id_endpoint(
    _: Request,
    user_id: UUID,
    handler=Depends(lambda: user_container.get_user_by_id_handler),
):
    return handler.execute(user_id)


async def get_all_users_endpoint(
    _: Request, handler=Depends(lambda: user_container.get_all_users_handler)
):
    return handler.execute()
