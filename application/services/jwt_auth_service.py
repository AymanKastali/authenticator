from application.ports.jwt_token_service_port import JwtTokenServicePort
from application.ports.user_repository import UserRepositoryPort
from domain.entities.jwt_token_payload import JwtTokenPayload
from domain.entities.user import User
from domain.utils.date_time_utils import (
    expires_after_days,
    expires_after_minutes,
)
from domain.value_objects.email import Email
from domain.value_objects.jwt_token_type import JwtTokenType


class JwtAuthService:
    def __init__(
        self, user_repo: UserRepositoryPort, jwt_service: JwtTokenServicePort
    ):
        self.user_repo = user_repo
        self.jwt_service = jwt_service

    def _authenticate_user_local(self, email: Email, password: str) -> User:
        user = self.user_repo.get_user_by_email(email)
        if not user or not user.active or not user.verify_password(password):
            raise ValueError("Invalid credentials")
        return user

    def generate_access_token(self, user: User) -> str:
        payload = JwtTokenPayload.create(
            sub=user.uid,
            email=user.email,
            typ=JwtTokenType.ACCESS,
            roles=list(user.roles),
            exp=expires_after_minutes(7),
        )
        access_token: str = self.jwt_service.sign(payload)
        return access_token

    def generate_refresh_token(self, user: User) -> str:
        payload = JwtTokenPayload.create(
            sub=user.uid,
            email=user.email,
            typ=JwtTokenType.REFRESH,
            roles=list(user.roles),
            exp=expires_after_days(7),
        )
        refresh_token: str = self.jwt_service.sign(payload)
        return refresh_token

    def generate_jwt_tokens(self, user: User) -> dict[str, str]:
        at = self.generate_access_token(user)
        rt = self.generate_refresh_token(user)
        return {"access_token": at, "refresh_token": rt}

    def execute(self, email: str, password: str):
        user: User = self._authenticate_user_local(
            email=Email.from_string(email), password=password
        )
        return self.generate_jwt_tokens(user)
