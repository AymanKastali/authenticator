from adapters.controllers.user.get_all import GetAllUsersController
from adapters.controllers.user.get_by_id import GetUserByIdController
from application.use_cases.user.get_all import GetAllUsersUseCase
from application.use_cases.user.get_by_id import GetUserByIdUseCase
from delivery.db.in_memory.repositories import get_in_memory_user_repository
from delivery.web.fastapi.api.v1.handlers.user.get_all import GetAllUsersHandler
from delivery.web.fastapi.api.v1.handlers.user.get_by_id import (
    GetUserByIdHandler,
)


class UserContainer:
    def __init__(self):
        # Repositories
        self.user_repo = get_in_memory_user_repository()

        # Use cases
        self.get_user_by_id_uc = GetUserByIdUseCase(user_repo=self.user_repo)
        self.get_all_users_uc = GetAllUsersUseCase(user_repo=self.user_repo)

        # Controllers
        self.get_user_by_id_controller = GetUserByIdController(
            use_case=self.get_user_by_id_uc
        )
        self.get_all_users_controller = GetAllUsersController(
            use_case=self.get_all_users_uc
        )

        # Handlers
        self.get_user_by_id_handler = GetUserByIdHandler(
            controller=self.get_user_by_id_controller
        )
        self.get_all_users_handler = GetAllUsersHandler(
            controller=self.get_all_users_controller
        )
