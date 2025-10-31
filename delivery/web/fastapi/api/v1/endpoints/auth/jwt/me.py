from typing import Annotated

from fastapi import Depends

from adapters.dto.responses.auth.jwt.me import ReadMeOutDto
from delivery.bootstrap.containers.auth import jwt_auth_container
from delivery.web.fastapi.api.v1.dependencies.jwt.auth import get_current_user


async def read_me_endpoint(
    current_user: Annotated[ReadMeOutDto, Depends(get_current_user)],
    handler=Depends(lambda: jwt_auth_container.read_me_handler),
):
    return handler.execute(user_id=current_user.as_uuid())
