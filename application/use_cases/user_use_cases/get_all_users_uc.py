from application.dto.user_dto import PersistenceUserDto, PublicUserDto
from application.mappers.user_mapper import UserMapper
from application.ports.user_repository import UserRepositoryPort


class GetAllUsersUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def execute(self) -> list[PublicUserDto]:
        users: list[PersistenceUserDto] = self.user_repo.get_all_users()
        users_dto: list[PublicUserDto] = [
            UserMapper.to_public_dto_from_persistence(user) for user in users
        ]
        return users_dto
