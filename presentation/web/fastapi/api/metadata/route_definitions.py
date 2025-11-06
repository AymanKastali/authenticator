from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Sequence

from fastapi import Response
from fastapi.datastructures import DefaultPlaceholder
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from presentation.web.fastapi.api.metadata.http_methods import HttpMethod


@dataclass
class Route:
    """
    Represents a FastAPI route with all optional parameters supported by add_api_route.
    """

    name: str
    path: str
    endpoint: Callable[..., Any]
    status_code: int
    methods: Sequence[HttpMethod] = field(default_factory=list)
    tags: Sequence[Enum] = field(default_factory=list)
    summary: str | None = None
    deprecated: bool | None = None
    response_model: Any = None
    description: str | None = None
    response_class: type[Response] | DefaultPlaceholder = JSONResponse
    responses: dict[int | str, dict[str, Any]] | None = None
    dependencies: Sequence[Depends] | None = None
