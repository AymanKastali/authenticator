from adapters.dto.responses.auth.session.session import SessionOutDto
from adapters.dto.responses.generic.success.item import ItemOutDto
from delivery.web.fastapi.api.metadata.http_methods import HttpMethod
from delivery.web.fastapi.api.metadata.route_tags import RouteTag
from delivery.web.fastapi.api.v1.endpoints.app.deprecated import (
    deprecated_endpoint,
)
from delivery.web.fastapi.api.v1.utils.routes_utils import create_route

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
        response_model=ItemOutDto[SessionOutDto],
        description="Endpoint to login a user and receive a SessionEntity token.",
        deprecated=True,
    ),
]
