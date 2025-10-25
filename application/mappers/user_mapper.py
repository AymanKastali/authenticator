from datetime import datetime

from application.dto.user_dto import PersistenceUserDto, PublicUserDto, UserDto
from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.identifiers import UUIDId
from domain.value_objects.role import Role


class UserMapper:
    @staticmethod
    def to_public_dto(user: User) -> PublicUserDto:
        return PublicUserDto(
            uid=user.uid.to_string(),
            email=user.email.to_string(),
            active=user.active,
            verified=user.verified,
        )

    @staticmethod
    def to_user_dto(user: User) -> UserDto:
        return UserDto(
            uid=user.uid.to_string(),
            email=user.email.to_string(),
            active=user.active,
            verified=user.verified,
            created_at=str(user.created_at),
            updated_at=str(user.updated_at),
        )

    @staticmethod
    def to_persistence_dto(user: User) -> PersistenceUserDto:
        return PersistenceUserDto(
            uid=user.uid.to_string(),
            email=user.email.to_string(),
            hashed_password=user.hashed_password.value
            if user.hashed_password
            else None,
            active=user.active,
            verified=user.verified,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
            deleted_at=user.deleted_at.isoformat() if user.deleted_at else None,
            roles=[role.name for role in user.roles],
        )

    @staticmethod
    def to_public_dto_from_persistence(
        user: PersistenceUserDto,
    ) -> PublicUserDto:
        return PublicUserDto(
            uid=user.uid,
            email=user.email,
            active=user.active,
            verified=user.verified,
        )

    @staticmethod
    def to_user_dto_from_persistence(user: PersistenceUserDto) -> UserDto:
        return UserDto(
            uid=user.uid,
            email=user.email,
            active=user.active,
            verified=user.verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @staticmethod
    def to_entity_from_persistence(user: PersistenceUserDto) -> User:
        """
        Convert a PersistenceUserDto back into a domain User entity.
        """
        return User(
            uid=UUIDId.from_string(user.uid),
            email=Email.from_string(user.email),
            active=user.active,
            verified=user.verified,
            created_at=datetime.fromisoformat(user.created_at),
            updated_at=datetime.fromisoformat(user.updated_at),
            deleted_at=datetime.fromisoformat(user.deleted_at)
            if user.deleted_at
            else None,
            roles=[Role[name] for name in user.roles]
            if user.roles
            else [Role.USER],
        )
