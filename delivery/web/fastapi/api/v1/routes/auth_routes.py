from delivery.web.fastapi.api.route_metadata.http_methods import HttpMethod
from delivery.web.fastapi.api.route_metadata.route_definitions import Route
from delivery.web.fastapi.api.route_metadata.route_tags import RouteTag
from delivery.web.fastapi.api.v1.endpoints.auth_endpoints import (
    login_user_endpoint,
)

routes = [
    Route(
        name="login_user",
        path="/login",
        status_code=200,
        methods=[HttpMethod.POST],
        endpoint=login_user_endpoint,
        tags=[RouteTag.AUTH],
        summary="Login User",
        deprecated=False,
        response_model=dict,
        description="Endpoint to create a Flat",
    )
]
