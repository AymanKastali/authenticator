from typing import List

from application.dto.auth.jwt.auth_user import AuthUserDto
from application.dto.auth.jwt.token_user import TokenUserDto
from application.dto.user.public import PublicUserDto
from domain.entities.user import UserEntity
from domain.value_objects.date_time import DateTimeVo


class UserMapper:
    """Mapper for converting UserEntity to various DTOs."""

    # ----------------------- Helpers -----------------------
    @classmethod
    def _datetime_to_iso(cls, dt: DateTimeVo) -> str:
        return dt.value.isoformat()

    @classmethod
    def _datetime_to_iso_optional(cls, dt: DateTimeVo | None) -> str | None:
        """Convert optional DateTimeVo to ISO 8601 string, or None if missing."""
        return dt.value.isoformat() if dt else None

    @classmethod
    def _roles_to_list(cls, roles) -> List[str]:
        """Convert list of RoleVo to list of strings."""
        return [role.value for role in roles]

    # ----------------------- AuthUserDto -----------------------
    @classmethod
    def to_auth_dto(cls, user: UserEntity) -> AuthUserDto:
        return AuthUserDto(
            uid=user.uid.value,
            email=user.email.value,
            status=user.status.value,
            created_at=cls._datetime_to_iso(user.created_at),
            roles=cls._roles_to_list(user.roles),
        )

    # ----------------------- PublicUserDto -----------------------
    @classmethod
    def to_public_dto(cls, user: UserEntity) -> PublicUserDto:
        return PublicUserDto(
            uid=user.uid.value,
            email=user.email.value,
            status=user.status.value,
        )

    # ----------------------- TokenUserDto -----------------------
    @classmethod
    def to_token_dto(cls, user: UserEntity) -> TokenUserDto:
        return TokenUserDto(
            uid=user.uid.value,
            email=user.email.value,
            status=user.status.value,
            created_at=cls._datetime_to_iso(user.created_at),
            deleted_at=cls._datetime_to_iso_optional(user.deleted_at),
            roles=cls._roles_to_list(user.roles),
        )
