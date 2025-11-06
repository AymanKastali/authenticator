from presentation.web.fastapi.api.metadata.http_methods import HttpMethod
from presentation.web.fastapi.api.metadata.route_tags import RouteTag
from presentation.web.fastapi.api.v1.endpoints.user.get_all import (
    get_all_users_endpoint,
)
from presentation.web.fastapi.api.v1.endpoints.user.get_by_id import (
    get_user_by_id_endpoint,
)
from presentation.web.fastapi.api.v1.utils.routes_utils import create_route
from presentation.web.fastapi.schemas.response.generic.success.item import (
    ItemResponseSchema,
)
from presentation.web.fastapi.schemas.response.generic.success.paginated import (
    PaginatedResponseModel,
)
from presentation.web.fastapi.schemas.response.user.public import (
    PublicUserResponseSchema,
)

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
        response_model=ItemResponseSchema[PublicUserResponseSchema],
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
        response_model=PaginatedResponseModel[PublicUserResponseSchema],
        description="Endpoint to get all Users info.",
    ),
]
