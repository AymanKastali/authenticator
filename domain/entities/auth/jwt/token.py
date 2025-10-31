from dataclasses import dataclass, field

from domain.value_objects.jwt_payload import JwtPayloadVo


@dataclass(frozen=True, kw_only=True)
class JwtEntity:
    """Entity representing the full JWT (header + payload + signature)."""

    payload: JwtPayloadVo
    signature: str  # Cryptographic signature (opaque to domain)
    header: dict[str, str] = field(
        default_factory=lambda: {"alg": "HS256", "typ": "JWT"}
    )

    # --- entity identity ---
    @property
    def jti(self):
        """Entity identity = token's unique JTI."""
        return self.payload.jti

    # --- domain behavior ---
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return self.payload.is_expired()

    def to_primitives(self) -> dict:
        """Return serializable representation for infrastructure use."""
        return {
            "header": self.header,
            "payload": self.payload.to_primitives(),
            "signature": self.signature,
        }

    @classmethod
    def create_signed(
        cls,
        payload: JwtPayloadVo,
        signature: str,
        header: dict[str, str] | None = None,
    ):
        hdr = header or {"alg": "HS256", "typ": "JWT"}
        return cls(payload=payload, signature=signature, header=hdr)
