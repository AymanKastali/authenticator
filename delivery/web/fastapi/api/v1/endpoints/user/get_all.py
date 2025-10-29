from fastapi import Depends

from adapters.dto.responses.auth.jwt.me import ReadMeOutDto
from delivery.bootstrap.containers import user_container
from delivery.web.fastapi.api.v1.dependencies.jwt.user import (
    get_current_user,
)


async def get_all_users_endpoint(
    _: ReadMeOutDto = Depends(get_current_user),
    handler=Depends(lambda: user_container.get_all_users_handler),
):
    return handler.execute()
