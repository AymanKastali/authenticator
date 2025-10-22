from adapters.presenters.response_models.success_item_response_model import (
    ItemResponseModel,
)
from adapters.presenters.response_models.success_paginated_response_model import (
    PaginatedResponseModel,
)
from delivery.web.fastapi.api.metadata.http_methods import HttpMethod
from delivery.web.fastapi.api.metadata.route_definitions import Route
from delivery.web.fastapi.api.metadata.route_tags import RouteTag
from delivery.web.fastapi.api.v1.endpoints.user_endpoints import (
    get_all_users_endpoint,
    get_me_endpoint,
    get_user_by_id_endpoint,
)

routes = [
    Route(
        name="get_me",
        path="/me",
        status_code=200,
        methods=[HttpMethod.GET],
        endpoint=get_me_endpoint,
        tags=[RouteTag.USERS],
        summary="Get my User info",
        deprecated=False,
        response_model=ItemResponseModel[dict],
        description="Endpoint to get my own User info.",
    ),
    Route(
        name="get_user_by_id",
        path="/{user_id}",
        status_code=200,
        methods=[HttpMethod.GET],
        endpoint=get_user_by_id_endpoint,
        tags=[RouteTag.USERS],
        summary="Get User info by ID",
        deprecated=False,
        response_model=ItemResponseModel[dict],
        description="Endpoint to get User info by ID.",
    ),
    Route(
        name="get_all_users",
        path="/",
        status_code=200,
        methods=[HttpMethod.GET],
        endpoint=get_all_users_endpoint,
        tags=[RouteTag.USERS],
        summary="Get all Users info",
        deprecated=False,
        response_model=PaginatedResponseModel[dict],
        description="Endpoint to get all Users info.",
    ),
]
