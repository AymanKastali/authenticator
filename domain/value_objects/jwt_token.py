from dataclasses import dataclass

from domain.utils.date_time import utc_now
from domain.value_objects.jwt_payload import JwtPayload


@dataclass(frozen=True)
class JwtToken:
    """
    Domain entity representing a JWT token.
    Encapsulates the token string and its payload.
    """

    value: str  # The actual JWT string
    payload: JwtPayload  # The decoded payload

    def is_expired(self) -> bool:
        """Check if the token is expired based on its payload."""
        return utc_now() > self.payload.exp

    def is_access_token(self) -> bool:
        """Check if this token is an access token."""
        return self.payload.type == "access"

    def is_refresh_token(self) -> bool:
        """Check if this token is a refresh token."""
        return self.payload.type == "refresh"

    def get_user_id(self) -> str:
        """Get the user ID (sub claim) from the payload."""
        return self.payload.sub

    def get_roles(self) -> list[str]:
        """Get the roles from the payload, if any."""
        return self.payload.roles or []

    def to_dict(self) -> dict:
        """Return a JSON-serializable dict of the token."""
        payload_dict = self.payload.to_dict()
        # Convert datetime fields to ISO strings
        for key in ["iat", "exp", "nbf"]:
            if payload_dict.get(key):
                payload_dict[key] = payload_dict[key].isoformat()
        return {
            "token": self.value,
            "payload": payload_dict,
        }

    def get_value(self) -> str:
        """Return only the raw JWT string."""
        return self.value
