from enum import IntEnum


class DomainErrorCodeEnum(IntEnum):
    DOMAIN = 1000  # Catch-all unknown domain error
    DOMAIN_VALIDATION = (
        1100  # 1=Domain, 1=Validation, 0=General, 0=Second error
    )
    INVALID_VALUE = 1101  # 1=Domain, 0=Validation, 0=General, 1=First error
    REQUIRED = 1102  # 1=Domain, 0=Validation, 0=General, 2=First error
    MAX_LENGTH_EXCEEDED = (
        1103  # 1=Domain, 0=Validation, 0=General, 2=First error
    )
    INVALID_TYPE = 1104  # 1=Domain, 0=Validation, 0=General, 1=First error
    PASSWORD_ERROR = 1105  # 1=Domain, 0=Validation, 0=General, 1=First error
