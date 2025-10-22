from uuid import UUID

from application.dto.user_dto.user_dto import UserDTO
from application.ports.user_repository import UserRepositoryPort
from domain.entities.user import User
from domain.value_objects.uids import UUIDId


class GetUserMeUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def execute(self, user_id: UUID) -> UserDTO:
        user_id_vo = UUIDId(user_id)
        user: User | None = self.user_repo.get_user_by_id(user_id_vo)
        if user is None:
            raise ValueError("User not found")

        user_dto: UserDTO = UserDTO.from_entity(user)
        return user_dto
