from domain.entities.user import UserEntity
from domain.interfaces.user_factory import UserFactoryInterface
from domain.value_objects.date_time import DateTimeVo
from domain.value_objects.email import EmailVo
from domain.value_objects.hashed_password import HashedPasswordVo
from domain.value_objects.identifiers import UUIDVo
from domain.value_objects.role import RoleVo
from domain.value_objects.user_status import UserStatusVo


class UserFactory(UserFactoryInterface):
    """Concrete factory for creating UserEntity instances."""

    def create_local_user(
        self,
        email: EmailVo,
        hashed_password: HashedPasswordVo,
        roles: list[RoleVo] | None = None,
    ) -> UserEntity:
        now = DateTimeVo.now()
        uid = UUIDVo.new()
        user_roles = roles or [RoleVo.USER]

        return UserEntity(
            uid=uid,
            _email=email,
            _hashed_password=hashed_password,
            _status=UserStatusVo.PENDING_VERIFICATION,
            created_at=now,
            updated_at=now,
            deleted_at=None,
            roles=user_roles,
        )

    def create_external_user(
        self, email: EmailVo, roles: list[RoleVo] | None = None
    ) -> UserEntity:
        now = DateTimeVo.now()
        uid = UUIDVo.new()
        user_roles = roles or [RoleVo.USER]

        return UserEntity(
            uid=uid,
            _email=email,
            _hashed_password=None,
            _status=UserStatusVo.VERIFIED,
            created_at=now,
            updated_at=now,
            deleted_at=None,
            roles=user_roles,
        )
