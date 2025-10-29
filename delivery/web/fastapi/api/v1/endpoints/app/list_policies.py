from fastapi import Depends

from adapters.dto.responses.auth.jwt.me import ReadMeOutDto
from delivery.bootstrap.containers import app_container
from delivery.web.fastapi.api.v1.dependencies.jwt.user import (
    get_current_user,
)


async def list_policies_endpoint(
    _: ReadMeOutDto = Depends(get_current_user),
    handler=Depends(lambda: app_container.list_policies_handler),
):
    return handler.execute()
