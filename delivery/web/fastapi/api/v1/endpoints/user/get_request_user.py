from typing import Annotated

from fastapi import Depends

from adapters.dto.response_dto.user_response_models import (
    AuthenticatedUserResponseModel,
)
from delivery.bootstrap.containers import user_feature_container
from delivery.web.fastapi.api.v1.dependencies.jwt.user import (
    get_current_user,
)


async def get_request_user_endpoint(
    current_user: Annotated[
        AuthenticatedUserResponseModel, Depends(get_current_user)
    ],
    handler=Depends(lambda: user_feature_container.get_request_user_handler),
):
    return handler.execute(user_id=current_user.as_uuid())
