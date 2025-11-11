from uuid import UUID

from application.dto.user.public import PublicUserDto
from application.mappers.user import UserMapper
from domain.entities.user import UserEntity
from domain.services.user.query_user import QueryUser
from domain.value_objects.identifiers import UUIDVo


class GetUserByIdUseCase:
    def __init__(self, query_user: QueryUser):
        self._query_user = query_user

    async def execute(self, user_id: UUID) -> PublicUserDto:
        uuid_vo = UUIDVo.from_uuid(user_id)

        user: UserEntity | None = await self._query_user.get_user_by_id(uuid_vo)

        if user is None:
            raise ValueError("User not found")
        if not user.active:
            raise ValueError("User is inactive")

        return UserMapper.to_public_dto_from_entity(user)
