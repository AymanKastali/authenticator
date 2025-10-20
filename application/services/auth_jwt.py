from application.ports.jwt_token_service import JwtTokenServicePort
from application.ports.user_repository import UserRepositoryPort
from domain.entities.user import User
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.uids import UUIDId


class JwtAuthService:
    def __init__(
        self, user_repo: UserRepositoryPort, jwt_service: JwtTokenServicePort
    ):
        self.user_repo = user_repo
        self.jwt_service = jwt_service

    def authenticate_local(
        self, email_address: EmailAddress, password: str
    ) -> User | None:
        user = self.user_repo.find_by_email(email_address)
        if not user or not user.is_active or not user.verify_password(password):
            return None
        return user

    def generate_tokens(self, user_id: UUIDId) -> dict:
        """Return both access and refresh tokens."""
        return {
            "access_token": self.jwt_service.generate_access_token(
                user_id.value
            ),
            "refresh_token": self.jwt_service.generate_refresh_token(
                user_id.value
            ),
        }

    def refresh_access_token(self, refresh_token: str) -> dict | None:
        """Generate new access token from valid refresh token."""
        user_id = self.jwt_service.verify_refresh_token(refresh_token)
        if not user_id:
            return None
        return {
            "access_token": self.jwt_service.generate_access_token(user_id),
        }
