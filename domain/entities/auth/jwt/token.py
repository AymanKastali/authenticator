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

    def __post_init__(self):
        self.validate()

    # --- entity identity ---
    @property
    def jti(self) -> str:
        """Entity identity = token's unique JTI."""
        return self.payload.jti.to_string()

    # --- domain behavior ---
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return self.payload.is_expired()

    # --- validation methods ---
    def ensure_valid_signature(self):
        if not self.signature:
            raise ValueError("JWT signature cannot be empty")

    def ensure_valid_header(self):
        alg = self.header.get("alg")
        typ = self.header.get("typ")
        if alg != "HS256":
            raise ValueError(f"Unsupported algorithm: {alg}")
        if typ != "JWT":
            raise ValueError(f"Invalid token type: {typ}")

    def ensure_not_expired(self):
        if self.is_expired():
            raise ValueError("JWT is already expired")

    def validate(self) -> None:
        self.ensure_not_expired()
        self.ensure_valid_header()
        self.ensure_valid_signature()

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
