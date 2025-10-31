from datetime import datetime

from application.dto.user.me import CurrentUserDto
from application.dto.user.persistence import PersistenceUserDto
from application.dto.user.public import PublicUserDto
from domain.entities.user import UserEntity
from domain.value_objects.email import Email
from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.identifiers import UUIDId
from domain.value_objects.role import Role


class UserMapper:
    @staticmethod
    def to_user_dto_from_entity(user: UserEntity) -> CurrentUserDto:
        return CurrentUserDto(
            uid=user.uid.to_string(),
            email=user.email.to_string(),
            active=user.active,
            verified=user.verified,
            created_at=str(user.created_at),
            updated_at=str(user.updated_at),
        )

    @staticmethod
    def to_persistence_dto_from_entity(user: UserEntity) -> PersistenceUserDto:
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
        dto: PersistenceUserDto,
    ) -> PublicUserDto:
        return PublicUserDto(
            uid=dto.uid,
            email=dto.email,
            active=dto.active,
            verified=dto.verified,
        )

    @staticmethod
    def to_user_dto_from_persistence_dto(
        dto: PersistenceUserDto,
    ) -> CurrentUserDto:
        return CurrentUserDto(
            uid=dto.uid,
            email=dto.email,
            active=dto.active,
            verified=dto.verified,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    @staticmethod
    def to_entity_from_persistence(dto: PersistenceUserDto) -> UserEntity:
        """
        Convert a PersistenceUserDto back into a domain UserEntity entity.
        """
        return UserEntity(
            uid=UUIDId.from_string(dto.uid),
            email=Email.from_string(dto.email),
            hashed_password=HashedPassword(dto.hashed_password)
            if dto.hashed_password
            else None,
            active=dto.active,
            verified=dto.verified,
            created_at=datetime.fromisoformat(dto.created_at),
            updated_at=datetime.fromisoformat(dto.updated_at),
            deleted_at=datetime.fromisoformat(dto.deleted_at)
            if dto.deleted_at
            else None,
            roles=[Role[name] for name in dto.roles]
            if dto.roles
            else [Role.USER],
        )
