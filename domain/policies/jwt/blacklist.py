from domain.exceptions.domain_errors import DomainError
from domain.interfaces.jwt_policy import JwtPolicy
from domain.value_objects.identifiers import UUIDId


class JwtBlacklistPolicy(JwtPolicy):
    def enforce(self, jti: UUIDId, revoked_tokens: set[str]) -> None:
        str_jti = jti.to_string()
        if str_jti in revoked_tokens:
            raise DomainError(f"Token {str_jti} has been revoked")
