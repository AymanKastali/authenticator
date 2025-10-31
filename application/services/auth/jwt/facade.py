# application/facades/jwt_auth_facade.py
from datetime import datetime, timedelta, timezone

from application.dto.auth.jwt.token import JwtDto
from application.mappers.jwt import JwtMapper
from application.ports.repositories.jwt import JwtRepositoryPort
from application.services.auth.authentication import AuthService
from application.services.auth.jwt.auth import JwtAuthService
from domain.entities.auth.jwt.token import JwtEntity
from domain.entities.user import UserEntity


class JwtAuthFacade:
    """Coordinates authentication, JWT creation, validation, and blacklist."""

    def __init__(
        self,
        auth_service: AuthService,
        jwt_auth_service: JwtAuthService,
        jwt_repo: JwtRepositoryPort,
    ):
        self._auth_service = auth_service
        self._jwt_auth_service = jwt_auth_service
        self._jwt_repo = jwt_repo

    # ------------------- Login / Token -------------------

    def _generate_jwt_tokens(self, user: UserEntity) -> dict[str, str]:
        access_token: JwtEntity = self._jwt_auth_service.create_access_token(
            user
        )
        refresh_token: JwtEntity = self._jwt_auth_service.create_refresh_token(
            user
        )
        return {
            "access_token": access_token.signature,
            "refresh_token": refresh_token.signature,
        }

    def login_user(self, email: str, password: str) -> dict[str, str]:
        user: UserEntity = self._auth_service.authenticate_user(email, password)
        return self._generate_jwt_tokens(user)

    def refresh_jwt_token(self, refresh_token: str) -> dict[str, str]:
        token: JwtEntity = self._jwt_auth_service.verify_refresh_token(
            refresh_token
        )
        user_id = token.payload.sub
        user: UserEntity = self._auth_service.get_user_by_id(user_id.to_uuid())
        return self._generate_jwt_tokens(user)

    # ------------------- Logout / Blacklist -------------------
    def logout(self, token: str) -> None:
        token_entity: JwtEntity = self._jwt_auth_service.verify_token(token)
        jti: str = token_entity.payload.jti.to_string()
        exp: float = token_entity.payload.exp.timestamp()

        expires_in: float = exp - datetime.now(timezone.utc).timestamp()
        expires_at: datetime = datetime.now(timezone.utc) + timedelta(
            seconds=expires_in
        )

        self._jwt_repo.add_token(jti=jti, expires_at=expires_at)

    # ------------------- Validation -------------------
    def is_token_valid(self, token: str) -> bool:
        token_entity: JwtEntity = self._jwt_auth_service.verify_token(token)

        if token_entity.is_expired():
            return False
        if self._jwt_repo.is_token_blacklisted(token_entity.jti.to_string()):
            return False
        return True

    def verify_jwt_token(
        self, token: str, subject: str | None = None
    ) -> JwtDto:
        token_entity: JwtEntity = self._jwt_auth_service.verify_token(
            token, subject
        )
        token_dto: JwtDto = JwtMapper.to_jwt_dto_from_entity(token_entity)
        return token_dto
