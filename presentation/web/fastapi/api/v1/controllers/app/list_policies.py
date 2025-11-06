from application.dto.policies.app import PolicyDto
from application.services.policy import PolicyService
from presentation.web.fastapi.schemas.response.generic.success.list import (
    ListResponseSchema,
)
from presentation.web.fastapi.schemas.response.policy.list import (
    PoliciesResponseSchema,
)


class ListPoliciesController:
    def __init__(self, service: PolicyService):
        self._service = service

    def execute(self) -> ListResponseSchema[PoliciesResponseSchema]:
        dto_list: list[PolicyDto] = self._service.list()
        policies = [
            PoliciesResponseSchema.model_validate(dto) for dto in dto_list
        ]
        return ListResponseSchema[PoliciesResponseSchema].build(
            data=policies,
            status_code=200,
            message="App Policies listed successfully",
        )
