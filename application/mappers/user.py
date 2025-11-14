from application.dto.auth.jwt.auth_user import AuthUserDto
from application.dto.auth.jwt.token_user import TokenUserDto
from application.dto.user.public import PublicUserDto
from domain.entities.user import UserEntity


class UserMapper:
    @staticmethod
    def to_auth_user_dto_from_entity(user: UserEntity) -> AuthUserDto:
        return AuthUserDto(
            uid=user.uid.to_string(),
            email=user.email.to_string(),
            status=user.status,
            created_at=str(user.created_at),
            updated_at=str(user.updated_at),
            roles=[role.value for role in user.roles],
        )

    @staticmethod
    def to_public_dto_from_entity(user: UserEntity) -> PublicUserDto:
        return PublicUserDto(
            uid=user.uid.to_string(),
            email=user.email.to_string(),
            status=user.status,
        )

    @staticmethod
    def to_token_user_dto_from_entity(
        user: UserEntity,
    ) -> TokenUserDto:
        return TokenUserDto(
            uid=user.uid.to_string(),
            email=user.email.to_string(),
            status=user.status,
            created_at=user.created_at.to_iso(),
            updated_at=user.updated_at.to_iso(),
            deleted_at=user.deleted_at.to_iso() if user.deleted_at else None,
            roles=[role.value for role in user.roles],
        )
