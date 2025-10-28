from fastapi import Depends

from adapters.dto.response_dto.user_response_models import (
    AuthenticatedUserResponseModel,
)
from delivery.bootstrap.containers import user_feature_container
from delivery.web.fastapi.api.v1.dependencies.jwt.user import (
    get_current_user,
)


async def get_all_users_endpoint(
    _: AuthenticatedUserResponseModel = Depends(get_current_user),
    handler=Depends(lambda: user_feature_container.get_all_users_handler),
):
    return handler.execute()
