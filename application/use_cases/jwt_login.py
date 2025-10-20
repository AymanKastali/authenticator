from application.services.auth_jwt import JwtAuthService
from domain.entities.user import User
from domain.value_objects.email_address import EmailAddress


class JwtLoginUseCase:
    def __init__(self, jwt_auth_service: JwtAuthService):
        self.jwt_auth_service = jwt_auth_service

    def execute(self, email_address: str, password: str) -> dict:
        user: User | None = self.jwt_auth_service.authenticate_local(
            EmailAddress(email_address), password
        )
        if not user:
            raise ValueError("Invalid credentials")
        return self.jwt_auth_service.generate_tokens(user.uid)
