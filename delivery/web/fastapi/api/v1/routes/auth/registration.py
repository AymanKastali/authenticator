from adapters.dto.response_dto.success_item_response_model import (
    ItemResponseModel,
)
from adapters.dto.response_dto.user_response_models import (
    RegisteredUserResponseModel,
)
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
        summary="Login User via Session",
        response_model=ItemResponseModel[RegisteredUserResponseModel],
        description="Endpoint to login a user and receive a Session token.",
    )
]
