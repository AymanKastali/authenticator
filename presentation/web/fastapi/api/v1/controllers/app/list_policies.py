from itertools import groupby

from application.dto.policies.app import PolicyDescriptionDto
from application.services.policy import PolicyService
from presentation.web.fastapi.schemas.response.generic.success.list import (
    ListResponseSchema,
)
from presentation.web.fastapi.schemas.response.policy.list import (
    PoliciesResponseSchema,
    PolicySchema,
)


class ListPoliciesController:
    def __init__(self, service: PolicyService):
        self._service = service

    def execute(self) -> ListResponseSchema[PoliciesResponseSchema]:
        dto_list: list[PolicyDescriptionDto] = self._service.list()

        dto_list.sort(key=lambda x: x.category)
        grouped = groupby(dto_list, key=lambda x: x.category)

        response = [
            PoliciesResponseSchema(
                category=category,
                policies=[
                    PolicySchema(name=dto.name, parameters=dto.parameters)
                    for dto in group
                ],
            )
            for category, group in grouped
        ]

        return ListResponseSchema[PoliciesResponseSchema].build(
            data=response,
            status_code=200,
            message="App Policies listed successfully",
        )
