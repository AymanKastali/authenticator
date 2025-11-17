from uuid import UUID

from application.dto.user.public import PublicUserDto
from application.mappers.user import UserMapper
from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import UserNotFoundError
from domain.factories.value_objects.uuid import UUIDVoFactory
from domain.ports.repositories.user import UserRepositoryPort


class GetUserByIdUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self._user_repo = user_repo

    async def execute(self, user_id: UUID) -> PublicUserDto:
        uuid_vo = UUIDVoFactory.from_uuid(user_id)

        user: UserEntity | None = await self._user_repo.get_user_by_id(uuid_vo)

        if user is None:
            raise UserNotFoundError(uuid_vo.value)

        user.ensure_active()
        user.ensure_not_deleted()

        return UserMapper.to_public_dto(user)
