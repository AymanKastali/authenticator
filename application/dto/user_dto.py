from dataclasses import dataclass

from domain.entities.user import User


@dataclass(frozen=True)
class UserDTO:
    uid: str
    email_address: str
    is_active: bool
    active: bool
    verified: bool
    created_at: str
    updated_at: str
    hashed_password: str | None = None
    deleted_at: str | None = None

    @classmethod
    def from_entity(cls, user: User) -> "UserDTO":
        deleted_at = str(user.deleted_at) if user.deleted_at else None
        hashed_password = (
            user.hashed_password.value if user.hashed_password else None
        )

        return cls(
            uid=user.uid.value,
            email_address=user.email_address.value,
            is_active=user.is_active,
            active=user.active,
            verified=user.verified,
            created_at=str(user.created_at),
            updated_at=str(user.updated_at),
            deleted_at=deleted_at,
            hashed_password=hashed_password,
        )

    # def to_dict(self) -> dict:
    #     return {
    #         "bedroom_id": self.bedroom_id,
    #         "bed_id": self.bed_id,
    #         "bed_type": self.bed_type,
    #         "label": self.label,
    #         "status": self.status,
    #         "tenant_id": self.tenant_id,
    #     }

    # @classmethod
    # def dict_to_entity(cls, data: dict) -> BedEntity:
    #     """
    #     Reconstitute a BedEntity from a dictionary.
    #     Handles optional tenant_id.
    #     """
    #     status = BedStatusEnum(
    #         data.get("status", BedStatusEnum.AVAILABLE.value)
    #     )
    #     bed_type = BedTypeEnum(data.get("bed_type", BedTypeEnum.SINGLE.value))
    #     tenant_id = UUIDId(data["tenant_id"]) if data.get("tenant_id") else None

    #     return BedEntity(
    #         _bed_id=BedId(data["bed_id"]),
    #         _bedroom_id=BedroomId(data["bedroom_id"]),
    #         _label=data["label"],
    #         _status=status,
    #         _bed_type=bed_type,
    #         _tenant_id=tenant_id,
    #     )
