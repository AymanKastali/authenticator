from adapters.dto.responses.generic.success.list import ListOutDto
from adapters.dto.responses.policy.list import PoliciesOutDto
from delivery.web.fastapi.api.metadata.http_methods import HttpMethod
from delivery.web.fastapi.api.metadata.route_tags import RouteTag
from delivery.web.fastapi.api.v1.endpoints.app.list_policies import (
    list_policies_endpoint,
)
from delivery.web.fastapi.api.v1.utils.routes_utils import create_route

_LIST_POLICIES = "/policy"

routes = [
    create_route(
        name="list_policies",
        path=_LIST_POLICIES,
        status_code=200,
        methods=[HttpMethod.GET],
        endpoint=list_policies_endpoint,
        tag=RouteTag.APP,
        summary="List App Policies",
        response_model=ListOutDto[PoliciesOutDto],
        description="Endpoint to list all app Policies.",
    )
]
