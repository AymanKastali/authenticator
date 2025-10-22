from application.dto.user_dto.public_user_dto import PublicUserDTO
from application.ports.user_repository import UserRepositoryPort
from domain.entities.user import User


class GetAllUsersUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def execute(self) -> list[PublicUserDTO]:
        users: list[User] = self.user_repo.get_all_users()
        users_dto: list[PublicUserDTO] = [
            PublicUserDTO.from_entity(user) for user in users
        ]
        return users_dto
