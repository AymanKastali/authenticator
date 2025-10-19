from adapters.gateways.authentication.jwt_service import JwtService
from application.dto.logged_in_user_dto import LoggedInUserDTO
from domain.entities.user import User
from domain.services.authentication import AuthenticationService
from domain.value_objects.email_address import EmailAddress


class LoginUserUseCase:
    def __init__(
        self, auth_service: AuthenticationService, jwt_service: JwtService
    ):
        self.auth_service = auth_service
        self.jwt_service = jwt_service

    def execute(self, email: str, password: str) -> LoggedInUserDTO | None:
        user: User | None = self.auth_service.authenticate_local(
            EmailAddress(email), password
        )
        if not user:
            return None
        token: str = self.jwt_service.generate_token(user.id.value)
        return LoggedInUserDTO(
            id=user.id.value, email=user.email.value, token=token
        )
