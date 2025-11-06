from dataclasses import dataclass, field

from domain.value_objects.jwt_payload import JwtPayloadVo


@dataclass(frozen=True, kw_only=True)
class JwtEntity:
    """Entity representing a full JWT (header + payload + signature)."""

    payload: JwtPayloadVo
    signature: str
    headers: dict[str, str] = field(
        default_factory=lambda: {"alg": "HS256", "typ": "JWT"}
    )

    def __post_init__(self):
        # Validate all invariants immediately after creation
        self._validate()

    # --- Entity identity ---
    @property
    def jti(self) -> str:
        """Unique token identifier."""
        return self.payload.jti.to_string()

    # --- Domain behavior ---
    def is_expired(self) -> bool:
        """Check if the JWT has expired."""
        return self.payload.is_expired()

    # --- Validation ---
    def _validate(self) -> None:
        self._ensure_signature()
        self._ensure_header()
        self._ensure_not_expired()

    def _ensure_signature(self) -> None:
        if not self.signature or not self.signature.strip():
            raise ValueError("JWT signature cannot be empty")

    def _ensure_header(self) -> None:
        alg = self.headers.get("alg")
        typ = self.headers.get("typ")
        if alg != "HS256":
            raise ValueError(f"Unsupported algorithm: {alg}")
        if typ != "JWT":
            raise ValueError(f"Invalid token type: {typ}")

    def _ensure_not_expired(self) -> None:
        if self.is_expired():
            raise ValueError("JWT is expired")

    # --- Utility ---
    def to_primitives(self) -> dict:
        """Return a fully serializable representation for infrastructure use."""
        return {
            "headers": dict(self.headers),
            "payload": self.payload.to_primitives(),
            "signature": self.signature,
        }

    @classmethod
    def create_signed(
        cls,
        payload: JwtPayloadVo,
        signature: str,
        headers: dict[str, str] | None = None,
    ) -> "JwtEntity":
        """Factory method to create a signed JWT with optional custom headers."""
        hdr = headers or {"alg": "HS256", "typ": "JWT"}
        return cls(payload=payload, signature=signature, headers=hdr)

    # --- Optional: Convenience for domain checks ---
    def ensure_active(self) -> None:
        """Raise if the JWT is expired or signature/header invalid."""
        self._validate()
