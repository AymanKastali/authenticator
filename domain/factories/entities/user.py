from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import (
    DomainRuleViolationError,
    InvalidValueError,
)
from domain.factories.value_objects.date_time import DateTimeVoFactory
from domain.factories.value_objects.uuid import UUIDVoFactory
from domain.interfaces.user_factory import UserEntityFactoryInterface
from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.email import EmailVo
from domain.value_objects.hashed_password import HashedPasswordVo
from domain.value_objects.role import RoleVo
from domain.value_objects.user_status import UserStatusVo


class UserEntityFactory(UserEntityFactoryInterface):
    """Factory responsible for constructing UserEntity with full invariant validation."""

    @classmethod
    def create(
        cls,
        *,
        email: EmailVo,
        status: UserStatusVo,
        hashed_password: HashedPasswordVo | None = None,
        deleted_at: DateTimeVo | None = None,
        roles: list[RoleVo],
    ) -> UserEntity:
        uid = UUIDVoFactory.new()
        created_at = DateTimeVoFactory.now()
        cls._validate_dates(created_at, deleted_at)
        cls._validate_roles(roles)
        cls._validate_status_invariants(status, deleted_at)

        return UserEntity(
            uid=uid,
            _email=email,
            _hashed_password=hashed_password,
            _status=status,
            created_at=created_at,
            deleted_at=deleted_at,
            roles=roles,
        )

    # ----------------- Mini Validators -----------------
    @staticmethod
    def _validate_dates(created_at: DateTimeVo, deleted_at: DateTimeVo | None):
        if created_at.is_future():
            raise InvalidValueError(
                "created_at", "created_at cannot be in the future"
            )

        if deleted_at and deleted_at.is_future():
            raise InvalidValueError(
                "deleted_at", "deleted_at cannot be in the future"
            )

    @staticmethod
    def _validate_roles(roles: list[RoleVo]):
        if not roles or any(not isinstance(r, RoleVo) for r in roles):
            raise InvalidValueError(
                "roles", "User must have at least one valid role"
            )

    @staticmethod
    def _validate_status_invariants(
        status: UserStatusVo, deleted_at: DateTimeVo | None
    ):
        if status == UserStatusVo.VERIFIED and status != UserStatusVo.ACTIVE:
            # Defensive: “verified but inactive” never allowed
            raise DomainRuleViolationError(
                message="Inactive users cannot be verified",
                rule_name="UserStatusRule",
            )
        # Soft-deleted should not be ACTIVE or VERIFIED
        if deleted_at is not None and status in {
            UserStatusVo.ACTIVE,
            UserStatusVo.VERIFIED,
        }:
            raise DomainRuleViolationError(
                message="Deleted user cannot be ACTIVE/VERIFIED",
                rule_name="UserDeletionStatusRule",
            )
