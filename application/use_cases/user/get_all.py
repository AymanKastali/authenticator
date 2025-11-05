from application.dto.user.persistence import PersistenceUserDto
from application.dto.user.public import PublicUserDto
from application.mappers.user import UserMapper
from application.ports.repositories.user import UserRepositoryPort
from domain.entities.user import UserEntity


class GetAllUsersUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    async def execute(self) -> list[PublicUserDto]:
        persistence_users: list[
            PersistenceUserDto
        ] = await self.user_repo.get_all_users()

        domain_users = []
        for dto in persistence_users:
            user_entity: UserEntity = UserMapper.to_entity_from_persistence(dto)

            if user_entity.active is False:
                continue

            domain_users.append(user_entity)

        users_dto: list[PublicUserDto] = [
            UserMapper.to_public_dto_from_entity(user) for user in domain_users
        ]

        return users_dto
