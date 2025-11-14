from presentation.web.fastapi.api.metadata.http_methods import HttpMethod
from presentation.web.fastapi.api.metadata.route_tags import RouteTag
from presentation.web.fastapi.api.v1.endpoints.auth.authenticate.register import (
    register_user_endpoint,
)
from presentation.web.fastapi.api.v1.utils.routes_utils import create_route
from presentation.web.fastapi.schemas.response.generic.success.item import (
    ItemResponseSchema,
)
from presentation.web.fastapi.schemas.response.user.registered import (
    RegisteredUserResponseSchema,
)

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
        response_model=ItemResponseSchema[RegisteredUserResponseSchema],
        description="Endpoint to login a user and receive a SessionEntity token.",
    )
]
