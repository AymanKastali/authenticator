from adapters.dto.responses.generic.success.item import ItemOutDto
from adapters.dto.responses.user.registered import RegisteredUserOutDto
from delivery.web.fastapi.api.metadata.http_methods import HttpMethod
from delivery.web.fastapi.api.metadata.route_tags import RouteTag
from delivery.web.fastapi.api.v1.endpoints.auth.registration.register import (
    register_user_endpoint,
)
from delivery.web.fastapi.api.v1.utils.routes_utils import create_route

_REGISTER = "/register"

routes = [
    create_route(
        name="register_user",
        path=_REGISTER,
        status_code=201,
        methods=[HttpMethod.POST],
        endpoint=register_user_endpoint,
        tag=RouteTag.AUTH,
        summary="Login UserEntity via SessionEntity",
        response_model=ItemOutDto[RegisteredUserOutDto],
        description="Endpoint to login a user and receive a SessionEntity token.",
    )
]
