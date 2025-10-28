from dataclasses import dataclass


@dataclass(frozen=True)
class PersistenceSessionDto:
    session_id: str
    user_id: str
    # expires_at: str
