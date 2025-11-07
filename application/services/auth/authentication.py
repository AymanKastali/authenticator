from domain.entities.user import UserEntity
from domain.services.user import UserDomainService
from domain.value_objects.email import EmailVo
from domain.value_objects.identifiers import UUIDVo


class AuthService:
    """Service for authentication and fetching authenticated user data."""

    def __init__(self, user_service: UserDomainService):
        self._user_service = user_service

    async def authenticate_user(
        self, email: EmailVo, password: str
    ) -> UserEntity:
        return await self._user_service.authenticate_user(email, password)

    async def get_user_by_id(self, user_id: UUIDVo) -> UserEntity:
        user: UserEntity | None = await self._user_service.get_user_by_id(
            user_id
        )
        if not user:
            raise ValueError("User not found")
        return user

    async def get_user_by_email(self, email: EmailVo) -> UserEntity:
        user: UserEntity | None = await self._user_service.get_user_by_email(
            email
        )
        if not user:
            raise ValueError("User not found")
        return user
