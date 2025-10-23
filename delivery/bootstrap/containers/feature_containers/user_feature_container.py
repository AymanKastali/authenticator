from adapters.controllers.user_controllers.get_all_users_controller import (
    GetAllUsersController,
)
from adapters.controllers.user_controllers.get_user_by_id_controller import (
    GetUserByIdController,
)
from adapters.controllers.user_controllers.get_user_me_controller import (
    GetUserMeController,
)
from application.use_cases.user_use_cases.get_all_users_uc import (
    GetAllUsersUseCase,
)
from application.use_cases.user_use_cases.get_user_by_id_uc import (
    GetUserByIdUseCase,
)
from application.use_cases.user_use_cases.get_user_me_uc import GetUserMeUseCase
from delivery.db.in_memory.repositories import get_in_memory_user_repository
from delivery.web.fastapi.api.v1.handlers.user_handlers.get_all_users_handler import (
    GetAllUsersHandler,
)
from delivery.web.fastapi.api.v1.handlers.user_handlers.get_user_by_id_handler import (
    GetUserByIdHandler,
)
from delivery.web.fastapi.api.v1.handlers.user_handlers.get_user_me_handler import (
    GetUserMeHandler,
)


class UserFeatureContainer:
    def __init__(self):
        # Repositories
        self.user_repo = get_in_memory_user_repository()

        # Use cases
        self.get_user_by_id_uc = GetUserByIdUseCase(user_repo=self.user_repo)
        self.get_all_users_uc = GetAllUsersUseCase(user_repo=self.user_repo)
        self.get_user_me_uc = GetUserMeUseCase(user_repo=self.user_repo)

        # Controllers
        self.get_user_by_id_controller = GetUserByIdController(
            use_case=self.get_user_by_id_uc
        )
        self.get_all_users_controller = GetAllUsersController(
            use_case=self.get_all_users_uc
        )
        self.get_user_me_controller = GetUserMeController(
            use_case=self.get_user_me_uc
        )

        # Handlers
        self.get_user_by_id_handler = GetUserByIdHandler(
            controller=self.get_user_by_id_controller
        )
        self.get_all_users_handler = GetAllUsersHandler(
            controller=self.get_all_users_controller
        )
        self.get_user_me_handler = GetUserMeHandler(
            controller=self.get_user_me_controller
        )
