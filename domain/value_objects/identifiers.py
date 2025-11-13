import base64
import os
from dataclasses import dataclass
from typing import ClassVar, Self
from uuid import UUID, uuid4


@dataclass(frozen=True)
class UUIDVo:
    value: UUID

    @staticmethod
    def new() -> "UUIDVo":
        return UUIDVo(uuid4())

    @classmethod
    def from_string(cls, value: str) -> Self:
        return cls(UUID(value))

    @classmethod
    def from_uuid(cls, value: UUID) -> Self:
        return cls(value)

    def to_string(self) -> str:
        return str(self.value)

    def to_uuid(self) -> UUID:
        return self.value


@dataclass(frozen=True)
class SessionIdVo:
    """
    Represents a session ID generated from a cryptographically secure
    random byte string, encoded using URL-safe Base64.

    This class follows security best practices by using a high-entropy
    CSPRNG and a URL-safe encoding.
    """

    # Define a Class Variable for the recommended random byte length
    # 32 bytes = 256 bits of entropy, which is exceptionally secure.
    RECOMMENDED_BYTE_LENGTH: ClassVar[int] = 32

    value: str

    @staticmethod
    def new() -> "SessionIdVo":
        """
        Generates a new session ID using cryptographically secure random bytes
        and encodes it using URL-safe Base64.
        """
        # 1. Generate cryptographically secure random bytes
        random_bytes = os.urandom(SessionIdVo.RECOMMENDED_BYTE_LENGTH)

        # 2. Encode the bytes using URL-safe Base64
        #    - urlsafe_b64encode handles characters like '+' and '/'
        #    - decode('utf-8') converts bytes to a string
        #    - rstrip(b'=') removes padding characters (best practice for tokens)
        encoded_string = (
            base64.urlsafe_b64encode(random_bytes)
            .rstrip(b"=")  # Remove padding for cleaner, shorter string
            .decode("utf-8")
        )

        return SessionIdVo(encoded_string)
