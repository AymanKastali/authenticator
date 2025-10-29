from adapters.dto.responses.policy.list import PoliciesOutDto
from application.dto.policies.app import PolicyDto
from application.services.policy import PolicyService


class ListPoliciesController:
    def __init__(self, service: PolicyService):
        self.service = service

    def execute(self) -> list[PoliciesOutDto]:
        policies: list[PolicyDto] = self.service.list()
        return [PoliciesOutDto.model_validate(policy) for policy in policies]
