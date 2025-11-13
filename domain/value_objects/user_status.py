from enum import auto

from domain.value_objects.string_enum import StringEnumVo


class UserStatusVo(StringEnumVo):
    ACTIVE = auto()
    INACTIVE = auto()
    PENDING_VERIFICATION = auto()
    VERIFIED = auto()
