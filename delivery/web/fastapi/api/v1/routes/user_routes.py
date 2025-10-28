from adapters.dto.response_dto.success_item_response_model import (
    ItemResponseModel,
)
from adapters.dto.response_dto.success_paginated_response_model import (
    PaginatedResponseModel,
)
from adapters.dto.response_dto.user_response_models import (
    PublicUserResponseModel,
    UserResponseModel,
)
from delivery.web.fastapi.api.metadata.http_methods import HttpMethod
from delivery.web.fastapi.api.metadata.route_tags import RouteTag
from delivery.web.fastapi.api.v1.endpoints.user.get_all import (
    get_all_users_endpoint,
)
from delivery.web.fastapi.api.v1.endpoints.user.get_by_id import (
    get_user_by_id_endpoint,
)
from delivery.web.fastapi.api.v1.endpoints.user.get_request_user import (
    get_request_user_endpoint,
)
from delivery.web.fastapi.api.v1.utils.routes_utils import create_route

_GET_REQUEST_USER = "/me"
_GET_USER_BY_ID = "/{user_id}"
_GET_ALL_USERS = "/"

routes = [
    create_route(
        name="get_request_user",
        path=_GET_REQUEST_USER,
        status_code=200,
        methods=[HttpMethod.GET],
        endpoint=get_request_user_endpoint,
        tag=RouteTag.USERS,
        summary="Get my User info",
        response_model=ItemResponseModel[UserResponseModel],
        description="Endpoint to get my own User info.",
    ),
    create_route(
        name="get_user_by_id",
        path=_GET_USER_BY_ID,
        status_code=200,
        methods=[HttpMethod.GET],
        endpoint=get_user_by_id_endpoint,
        tag=RouteTag.USERS,
        summary="Get User info by ID",
        response_model=ItemResponseModel[PublicUserResponseModel],
        description="Endpoint to get User info by ID.",
    ),
    create_route(
        name="get_all_users",
        path=_GET_ALL_USERS,
        status_code=200,
        methods=[HttpMethod.GET],
        endpoint=get_all_users_endpoint,
        tag=RouteTag.USERS,
        summary="Get all Users info",
        response_model=PaginatedResponseModel[PublicUserResponseModel],
        description="Endpoint to get all Users info.",
    ),
]
