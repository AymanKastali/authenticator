from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtConfig(BaseSettings):
    secret_key: SecretStr = Field(default=..., description="JWT secret key")
    private_key: SecretStr = Field(default=..., description="JWT private key")
    public_key: SecretStr = Field(default=..., description="JWT public key")
    algorithm: str = Field(default="RS256")
    issuer: str = Field(default="auth.myapp.com")
    audience: str = Field(default="api.myapp.com")
    leeway: int = Field(default=0)
    access_token_exp: int = Field(
        default=1800,
        description="Access token expiration in seconds (30 minutes)",
    )
    refresh_token_exp: int = Field(
        default=604800,
        description="Refresh token expiration in seconds (7 days)",
    )

    model_config = SettingsConfigDict(
        env_prefix="JWT_",
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Validators
    @field_validator("algorithm", "issuer", "audience")
    @classmethod
    def non_empty_string(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must be a non-empty string")
        return v

    @field_validator("leeway", "access_token_exp", "refresh_token_exp")
    @classmethod
    def non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("must be 0 or greater")
        return v
