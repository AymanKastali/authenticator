from enum import auto

from domain.value_objects.string_enum import StringEnumVo


class JwtStatusVo(StringEnumVo):
    ACTIVE = auto()
    REVOKED = auto()
    EXPIRED = auto()
