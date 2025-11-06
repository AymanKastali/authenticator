from uuid import UUID

from application.dto.auth.jwt.token_user import TokenUserDto
from application.mappers.user import UserMapper
from domain.entities.user import UserEntity
from domain.services.user import UserDomainService
from domain.value_objects.identifiers import UUIDVo


class GetAuthenticatedUserUseCase:
    def __init__(self, user_service: UserDomainService):
        self._user_service = user_service

    async def execute(self, user_id: UUID) -> TokenUserDto:
        uuid_vo = UUIDVo.from_uuid(user_id)

        user: UserEntity | None = await self._user_service.get_user_by_id(
            uuid_vo
        )

        if user is None:
            raise ValueError("User not found")
        if user.deleted:
            raise ValueError("User deleted")

        return UserMapper.to_token_user_dto_from_entity(user)
