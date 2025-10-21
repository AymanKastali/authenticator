from dataclasses import dataclass, field
from datetime import datetime

from domain.utils.date_time import utc_now
from domain.value_objects.role import Role


@dataclass(frozen=True, kw_only=True)
class JwtClaims:
    """Optional extra claims for JWTs, provided by the application layer or client."""

    roles: list[str] = field(default_factory=list)
    email: str | None = None
    username: str | None = None
    issuer: str | None = None
    audience: str | None = None
    not_before: datetime | None = None

    def __post_init__(self):
        # Validate roles: must be valid Role enum names or strings
        validated_roles = []
        for role in self.roles:
            if isinstance(role, Role):
                validated_roles.append(role.value)
            elif isinstance(role, str) and role in Role.values():
                validated_roles.append(role)
            else:
                raise ValueError(f"Invalid role: {role}")

        # Since dataclasses are frozen, use object.__setattr__
        object.__setattr__(self, "roles", validated_roles)

        if self.not_before is not None and self.not_before < utc_now():
            raise ValueError("not_before cannot be in the past")
