from adapters.dto.responses.generic.success.item import ItemOutDto
from adapters.dto.responses.generic.success.paginated import (
    PaginatedResponseModel,
)
from adapters.dto.responses.user.public import PublicUserOutDto
from delivery.web.fastapi.api.metadata.http_methods import HttpMethod
from delivery.web.fastapi.api.metadata.route_tags import RouteTag
from delivery.web.fastapi.api.v1.endpoints.user.get_all import (
    get_all_users_endpoint,
)
from delivery.web.fastapi.api.v1.endpoints.user.get_by_id import (
    get_user_by_id_endpoint,
)
from delivery.web.fastapi.api.v1.utils.routes_utils import create_route

_GET_USER_BY_ID = "/{user_id}"
_GET_ALL_USERS = "/"

routes = [
    create_route(
        name="get_user_by_id",
        path=_GET_USER_BY_ID,
        status_code=200,
        methods=[HttpMethod.GET],
        endpoint=get_user_by_id_endpoint,
        tag=RouteTag.USERS,
        summary="Get UserEntity info by ID",
        response_model=ItemOutDto[PublicUserOutDto],
        description="Endpoint to get UserEntity info by ID.",
    ),
    create_route(
        name="get_all_users",
        path=_GET_ALL_USERS,
        status_code=200,
        methods=[HttpMethod.GET],
        endpoint=get_all_users_endpoint,
        tag=RouteTag.USERS,
        summary="Get all Users info",
        response_model=PaginatedResponseModel[PublicUserOutDto],
        description="Endpoint to get all Users info.",
    ),
]
