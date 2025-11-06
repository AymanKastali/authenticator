from uuid import UUID

from application.dto.auth.jwt.auth_user import AuthUserDto
from application.mappers.user import UserMapper
from domain.services.user import UserDomainService
from domain.value_objects.email import EmailVo
from domain.value_objects.identifiers import UUIDVo


class AuthService:
    """Service for authentication and fetching authenticated user data."""

    def __init__(self, user_service: UserDomainService):
        self._user_service = user_service

    async def authenticate_user(self, email: str, password: str) -> AuthUserDto:
        email_vo = EmailVo.from_string(email)
        user = await self._user_service.authenticate_user(email_vo, password)
        return UserMapper.to_auth_user_dto_from_entity(user)

    async def get_user_by_id(self, user_id: UUID) -> AuthUserDto:
        uuid_vo = UUIDVo(user_id)
        user = await self._user_service.get_user_by_id(uuid_vo)
        if not user:
            raise ValueError("User not found")
        return UserMapper.to_auth_user_dto_from_entity(user)

    async def get_user_by_email(self, email: str) -> AuthUserDto:
        email_vo = EmailVo.from_string(email)
        user = await self._user_service.get_user_by_email(email_vo)
        if not user:
            raise ValueError("User not found")
        return UserMapper.to_auth_user_dto_from_entity(user)
