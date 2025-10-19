from dataclasses import dataclass


@dataclass(frozen=True)
class UserDTO:
    id: str
    email: str
    hashed_password: str | None
    is_active: bool
    active: bool
    verified: bool
    created_at: str
    updated_at: str
    deleted_at: str | None = None

    # @classmethod
    # def from_entity(cls, bed: BedEntity) -> "BedDTO":
    #     return cls(
    #         bedroom_id=str(bed.bedroom_id.value),
    #         bed_id=str(bed.bed_id.value),
    #         bed_type=bed.bed_type.value,
    #         label=bed.label,
    #         tenant_id=str(bed.tenant_id.value) if bed.tenant_id else None,
    #         status=bed.status.value,
    #     )

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
    #     tenant_id = UserId(data["tenant_id"]) if data.get("tenant_id") else None

    #     return BedEntity(
    #         _bed_id=BedId(data["bed_id"]),
    #         _bedroom_id=BedroomId(data["bedroom_id"]),
    #         _label=data["label"],
    #         _status=status,
    #         _bed_type=bed_type,
    #         _tenant_id=tenant_id,
    #     )
