from dataclasses import dataclass, field

from domain.utils.time import utc_now
from domain.value_objects.jwt_payload import JwtPayloadVo


@dataclass(frozen=True, kw_only=True)
class JwtEntity:
    """Entity representing the full JWT (header + payload + signature)."""

    payload: JwtPayloadVo
    signature: str  # Cryptographic signature (opaque to domain)
    header: dict[str, str] = field(
        default_factory=lambda: {"alg": "HS256", "typ": "JWT"}
    )

    def __post_init__(self):
        self._validate_signature()
        self._validate_header()
        self._validate_expiration()

    # --- entity identity ---
    @property
    def jti(self):
        """Entity identity = token's unique JTI."""
        return self.payload.jti

    # --- domain behavior ---
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return utc_now() >= self.payload.exp

    # --- validation methods ---
    def _validate_signature(self):
        if not self.signature:
            raise ValueError("JWT signature cannot be empty")

    def _validate_header(self):
        alg = self.header.get("alg")
        typ = self.header.get("typ")
        if alg != "HS256":
            raise ValueError(f"Unsupported algorithm: {alg}")
        if typ != "JWT":
            raise ValueError(f"Invalid token type: {typ}")

    def _validate_expiration(self):
        if self.is_expired():
            raise ValueError("JWT is already expired")

    # --- utility ---
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
