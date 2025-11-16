from uuid import UUID

from application.dto.user.public import PublicUserDto
from application.mappers.user import UserMapper
from application.services.user import UserQueryService
from domain.entities.user import UserEntity
from domain.factories.value_objects.uuid import UUIDVoFactory


class GetUserByIdUseCase:
    def __init__(self, user_query_service: UserQueryService):
        self._user_query_service = user_query_service

    async def execute(self, user_id: UUID) -> PublicUserDto:
        uuid_vo = UUIDVoFactory.from_uuid(user_id)

        user: UserEntity | None = await self._user_query_service.get_user_by_id(
            uuid_vo
        )

        if user is None:
            raise ValueError("User not found")
        if not user.is_active:
            raise ValueError("User is inactive")

        return UserMapper.to_public_dto(user)
