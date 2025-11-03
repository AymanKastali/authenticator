from typing import Annotated

from fastapi import Depends

from adapters.dto.responses.auth.jwt.authenticated_user import (
    AuthenticatedUserOutDto,
)
from adapters.dto.responses.generic.success.item import ItemOutDto
from delivery.web.fastapi.api.v1.dependencies.jwt import (
    get_current_authenticated_user,
)


async def get_authenticated_user_endpoint(
    authenticated_user: Annotated[
        AuthenticatedUserOutDto, Depends(get_current_authenticated_user)
    ],
):
    return ItemOutDto[AuthenticatedUserOutDto].build(
        data=authenticated_user,
        status_code=200,
        message="Authenticated User Data Fetched Successfully",
    )
