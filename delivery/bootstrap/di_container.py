from adapters.controllers.jwt.get_request_user_controller import (
    GetRequestUserController,
)
from adapters.gateways.authentication.jwt_service import JwtService
from application.use_cases.user_use_cases.get_request_user_uc import (
    GetRequestUserUseCase,
)
from delivery.bootstrap.domain_config_factory import DomainConfigFactory
from delivery.db.in_memory.repositories import get_in_memory_user_repository


class Container:
    def __init__(self):
        # Repositories
        self.user_repo = get_in_memory_user_repository()

        # Use cases
        self.get_user_use_case = GetRequestUserUseCase(user_repo=self.user_repo)

        # Controllers
        self.get_user_controller = GetRequestUserController(
            use_case=self.get_user_use_case
        )

        # Infrastructure
        self.jwt_service = JwtService(
            jwt_cfg=DomainConfigFactory.load_jwt_config()
        )


container = Container()
