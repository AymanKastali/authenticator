from typing import Annotated

from fastapi import Depends

from presentation.web.fastapi.api.v1.dependencies.security.jwt import (
    get_current_authenticated_user,
)
from presentation.web.fastapi.schemas.response.auth.jwt.authenticated_user import (
    AuthenticatedUserResponseSchema,
)
from presentation.web.fastapi.schemas.response.generic.success.item import (
    ItemResponseSchema,
)


async def get_authenticated_user_endpoint(
    authenticated_user: Annotated[
        AuthenticatedUserResponseSchema, Depends(get_current_authenticated_user)
    ],
):
    return ItemResponseSchema[AuthenticatedUserResponseSchema].build(
        data=authenticated_user,
        status_code=200,
        message="Authenticated User Data Fetched Successfully",
    )
