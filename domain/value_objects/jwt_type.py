from enum import auto

from domain.value_objects.string_enum import StringEnumVo


class JwtTypeVo(StringEnumVo):
    ACCESS = auto()
    REFRESH = auto()
