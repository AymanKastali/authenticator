from fastapi import Depends, Query

from adapters.dto.responses.auth.jwt.me import ReadMeOutDto
from delivery.bootstrap.containers import user_container
from delivery.web.fastapi.api.v1.dependencies.jwt.auth import (
    get_current_user,
)


async def get_all_users_endpoint(
    _: ReadMeOutDto = Depends(get_current_user),
    page: int = Query(default=1, ge=1, lt=1000),
    page_size: int = Query(default=20, ge=1, lt=50),
    handler=Depends(lambda: user_container.get_all_users_handler),
):
    return handler.execute(page, page_size)
