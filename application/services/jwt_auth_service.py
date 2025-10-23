from application.ports.jwt_token_service import JwtTokenServicePort
from application.ports.user_repository import UserRepositoryPort
from domain.entities.user import User
from domain.value_objects.email import Email
from domain.value_objects.jwt_claims import JwtClaims
from domain.value_objects.jwt_payload import JwtPayload
from domain.value_objects.uids import UUIDId


class JwtAuthService:
    def __init__(
        self, user_repo: UserRepositoryPort, jwt_service: JwtTokenServicePort
    ):
        self.user_repo = user_repo
        self.jwt_service = jwt_service

    def authenticate_local(self, email: Email, password: str) -> User | None:
        user = self.user_repo.get_user_by_email(email)
        if not user or not user.active or not user.verify_password(password):
            return None
        return user

    def generate_tokens(
        self, user_id: UUIDId, claims: JwtClaims | None = None
    ) -> dict:
        claims = claims or JwtClaims()
        return {
            "access_token": self.jwt_service.generate_access_token(
                user_id=user_id.to_string(), claims=claims
            ),
            "refresh_token": self.jwt_service.generate_refresh_token(
                user_id=user_id.to_string(), claims=claims
            ),
        }

    def refresh_access_token(self, refresh_token: str) -> dict | None:
        payload: JwtPayload | None = self.jwt_service.verify_refresh_token(
            refresh_token
        )
        if not payload:
            return None

        claims = JwtClaims(
            roles=payload.roles or [],
            email=payload.email,
            username=payload.username,
            issuer=payload.iss,
            audience=payload.aud,
        )
        return {
            "access_token": self.jwt_service.generate_access_token(
                payload.sub, claims
            )
        }
