from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> "datetime":
    return datetime.now(timezone.utc)


@dataclass
class DateTimeMixin:
    """
    Mixin for timestamp tracking.
    Adds created_at, updated_at, and deleted_at fields,
    along with helper methods to manage them.
    """

    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    deleted_at: datetime | None = None

    def mark_updated(self) -> None:
        """Refresh the 'updated_at' timestamp."""
        self.updated_at = utc_now()

    def mark_deleted(self) -> None:
        """Soft-delete the entity."""
        self.deleted_at = utc_now()
        self.mark_updated()

    def is_deleted(self) -> bool:
        """Check if this entity is soft-deleted."""
        return self.deleted_at is not None
