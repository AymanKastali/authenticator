from presentation.web.fastapi.api.metadata.http_methods import HttpMethod
from presentation.web.fastapi.api.metadata.route_tags import RouteTag
from presentation.web.fastapi.api.v1.endpoints.app.deprecated import (
    deprecated_endpoint,
)
from presentation.web.fastapi.api.v1.utils.routes_utils import create_route
from presentation.web.fastapi.schemas.response.auth.session.session import (
    SessionResponseSchema,
)
from presentation.web.fastapi.schemas.response.generic.success.item import (
    ItemResponseSchema,
)

_LOGIN = "/login/session"

routes = [
    create_route(
        name="session_login_user",
        path=_LOGIN,
        status_code=501,
        methods=[HttpMethod.POST],
        endpoint=deprecated_endpoint,
        tag=RouteTag.AUTH,
        summary="Login UserEntity via SessionEntity",
        response_model=ItemResponseSchema[SessionResponseSchema],
        description="Endpoint to login a user and receive a SessionEntity token.",
        deprecated=True,
    ),
]
