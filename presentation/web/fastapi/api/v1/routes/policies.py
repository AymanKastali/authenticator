from presentation.web.fastapi.api.metadata.http_methods import HttpMethod
from presentation.web.fastapi.api.metadata.route_tags import RouteTag
from presentation.web.fastapi.api.v1.endpoints.app.list_policies import (
    list_policies_endpoint,
)
from presentation.web.fastapi.api.v1.utils.routes_utils import create_route
from presentation.web.fastapi.schemas.response.generic.success.list import (
    ListResponseSchema,
)
from presentation.web.fastapi.schemas.response.policy.list import (
    PoliciesResponseSchema,
)

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
        response_model=ListResponseSchema[PoliciesResponseSchema],
        description="Endpoint to list all app Policies.",
    )
]
