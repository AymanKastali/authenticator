from adapters.controllers.policy.list import ListPoliciesController
from adapters.dto.responses.generic.success.list import ListOutDto
from adapters.dto.responses.policy.list import PoliciesOutDto


class ListPoliciesHandler:
    def __init__(self, controller: ListPoliciesController):
        self._controller = controller

    def execute(self) -> ListOutDto[PoliciesOutDto]:
        policies: list[PoliciesOutDto] = self._controller.execute()
        return ListOutDto[PoliciesOutDto].build(
            data=policies,
            status_code=200,
            message="App Policies listed successfully",
        )
