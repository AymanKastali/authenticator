from dataclasses import dataclass

from domain.value_objects.jwt_header import JwtHeaderVo
from domain.value_objects.jwt_payload import JwtPayloadVo


@dataclass(frozen=True, kw_only=True)
class JwtEntity:
    """Entity representing a full JWT (header + payload + signature)."""

    payload: JwtPayloadVo
    signature: str
    headers: JwtHeaderVo

    def __post_init__(self):
        self._validate()

    # --- Entity identity ---
    @property
    def jti(self) -> str:
        """Unique token identifier."""
        return self.payload.jti.to_string()

    # --- Validation ---
    def _validate(self) -> None:
        self._validate_signature()
        self._validate_payload()
        self._validate_headers()

    def _validate_signature(self):
        if not self.signature or not self.signature.strip():
            raise ValueError("JWT signature cannot be empty")

    def _validate_payload(self):
        self.payload.validate()

    def _validate_headers(self):
        self.headers.validate()

    # --- Utility ---
    def to_dict(self) -> dict:
        """Return a fully serializable representation for infrastructure use."""
        return {
            "headers": self.headers.to_dict(),
            "payload": self.payload.to_dict(),
            "signature": self.signature,
        }

    @classmethod
    def create_signed(
        cls, payload: JwtPayloadVo, signature: str, headers: JwtHeaderVo
    ) -> "JwtEntity":
        """Factory method to create a signed JWT with optional custom headers."""
        return cls(payload=payload, signature=signature, headers=headers)
