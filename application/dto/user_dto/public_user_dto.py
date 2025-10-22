from dataclasses import dataclass

from domain.entities.user import User


@dataclass(frozen=True)
class PublicUserDTO:
    uid: str
    email: str
    active: bool
    verified: bool = False

    @classmethod
    def from_entity(cls, user: User) -> "PublicUserDTO":
        return cls(
            uid=str(user.uid.value),
            email=user.email.value,
            active=user.active,
            verified=user.verified,
        )
