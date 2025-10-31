from typing import Annotated
from uuid import UUID

from fastapi import Depends

from adapters.dto.responses.auth.jwt.me import ReadMeOutDto
from delivery.bootstrap.containers import user_container
from delivery.web.fastapi.api.v1.dependencies.jwt.auth import get_current_user


async def get_user_by_id_endpoint(
    _: Annotated[ReadMeOutDto, Depends(get_current_user)],
    user_id: UUID,
    handler=Depends(lambda: user_container.get_user_by_id_handler),
):
    return handler.execute(user_id)
