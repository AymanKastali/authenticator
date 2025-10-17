from adapters.gateways.authentication.jwt_service import JwtService
from domain.services.authentication import AuthenticationService
from domain.value_objects.email_address import EmailAddress


class LoginUserUseCase:
    def __init__(
        self, auth_service: AuthenticationService, jwt_service: JwtService
    ):
        self.auth_service = auth_service
        self.jwt_service = jwt_service

    def execute(self, email: str, password: str) -> dict | None:
        user = self.auth_service.authenticate_local(
            EmailAddress(email), password
        )
        if not user:
            return None
        token = self.jwt_service.generate_token(user.id.value)
        return {"user_id": user.id.value, "token": token}
