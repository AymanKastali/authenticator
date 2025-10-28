from adapters.dto.response_dto.session_response_dto import SessionOutDto
from adapters.dto.response_dto.success_item_response_model import (
    ItemResponseModel,
)
from delivery.web.fastapi.api.metadata.http_methods import HttpMethod
from delivery.web.fastapi.api.metadata.route_tags import RouteTag
from delivery.web.fastapi.api.v1.endpoints.auth.session.login import (
    session_login_endpoint,
)
from delivery.web.fastapi.api.v1.utils.routes_utils import create_route

_LOGIN = "/login/session"

routes = [
    create_route(
        name="session_login_user",
        path=_LOGIN,
        status_code=200,
        methods=[HttpMethod.POST],
        endpoint=session_login_endpoint,
        tag=RouteTag.AUTH,
        summary="Login User via Session",
        response_model=ItemResponseModel[SessionOutDto],
        description="Endpoint to login a user and receive a Session token.",
    ),
]
