from typing import Callable, Type

from pydantic import BaseModel

from delivery.web.fastapi.api.metadata.http_methods import HttpMethod
from delivery.web.fastapi.api.metadata.route_definitions import Route
from delivery.web.fastapi.api.metadata.route_tags import RouteTag


def create_route(
    name: str,
    path: str,
    endpoint: Callable,
    methods: list[HttpMethod],
    response_model: Type[BaseModel],
    tag: RouteTag,
    summary: str | None = None,
    description: str | None = None,
    status_code: int = 200,
    deprecated: bool = False,
) -> Route:
    return Route(
        name=name,
        path=path,
        status_code=status_code,
        methods=methods,
        endpoint=endpoint,
        tags=[tag],
        summary=summary,
        deprecated=deprecated,
        response_model=response_model,
        description=description,
    )
