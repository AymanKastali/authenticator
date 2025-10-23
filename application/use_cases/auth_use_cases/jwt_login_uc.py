from application.services.jwt_auth_service import JwtAuthService
from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.jwt_claims import JwtClaims


class JwtLoginUseCase:
    def __init__(self, jwt_auth_service: JwtAuthService):
        self.jwt_auth_service = jwt_auth_service

    def execute(self, email: str, password: str) -> dict:
        user: User | None = self.jwt_auth_service.authenticate_local(
            Email(email), password
        )
        if not user:
            raise ValueError("Invalid credentials")

        claims: JwtClaims = JwtClaims(
            roles=[role.value for role in user.roles], email=user.email.value
        )
        tokens: dict = self.jwt_auth_service.generate_tokens(user.uid, claims)
        raw_tokens: dict = {
            "access_token": tokens["access_token"].get_value(),
            "refresh_token": tokens["refresh_token"].get_value(),
        }
        return raw_tokens
