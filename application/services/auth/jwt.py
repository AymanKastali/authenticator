from datetime import datetime, timedelta
from uuid import UUID

from application.dto.auth.jwt.token import JwtPayloadDto
from application.dto.user.persistence import PersistenceUserDto
from application.mappers.jwt import JwtPayloadMapper
from application.mappers.user import UserMapper
from application.ports.repositories.jwt import JwtRepositoryPort
from application.ports.repositories.user import UserRepositoryPort
from application.ports.services.jwt import JwtServicePort
from domain.entities.auth.jwt.token_payload import JwtTokenPayloadEntity
from domain.entities.user import UserEntity
from domain.utils.time import expires_after, utc_now, utc_now_time_stamp
from domain.value_objects.jwt_token_type import JwtTokenType


class JwtAuthService:
    def __init__(
        self,
        user_repo: UserRepositoryPort,
        jwt_repo: JwtRepositoryPort,
        jwt_service: JwtServicePort,
    ):
        self._user_repo = user_repo
        self._jwt_repo = jwt_repo
        self._jwt_service = jwt_service

    def _authenticate_user_local(
        self, email: str, password: str
    ) -> PersistenceUserDto:
        """Authenticate a user using local credentials."""
        user_dto = self._user_repo.get_user_by_email(email)
        if user_dto is None:
            raise ValueError("UserEntity not found")

        user_entity = UserMapper.to_entity_from_persistence(user_dto)

        if not user_entity.active:
            raise ValueError("UserEntity account is inactive")

        if not user_entity.verify_password(password):
            raise ValueError("Invalid credentials")

        return user_dto

    def _generate_access_token(self, user: UserEntity) -> str:
        payload = JwtTokenPayloadEntity.create(
            sub=user.uid,
            email=user.email,
            typ=JwtTokenType.ACCESS,
            roles=list(user.roles),
            exp=expires_after(minutes=30),
        )
        payload_dto = JwtPayloadMapper.to_dto_from_entity(payload)
        return self._jwt_service.sign(payload_dto)

    def _generate_refresh_token(self, user: UserEntity) -> str:
        payload = JwtTokenPayloadEntity.create(
            sub=user.uid,
            email=user.email,
            typ=JwtTokenType.REFRESH,
            roles=list(user.roles),
            exp=expires_after(days=7),
        )
        payload_dto = JwtPayloadMapper.to_dto_from_entity(payload)
        return self._jwt_service.sign(payload_dto)

    def _generate_jwt_tokens(self, user: UserEntity) -> dict[str, str]:
        return {
            "access_token": self._generate_access_token(user),
            "refresh_token": self._generate_refresh_token(user),
        }

    def login_user(self, email: str, password: str) -> dict[str, str]:
        """Authenticate and return JWT tokens."""
        user_dto = self._authenticate_user_local(email, password)
        user_entity = UserMapper.to_entity_from_persistence(user_dto)
        return self._generate_jwt_tokens(user_entity)

    def refresh_jwt_token(self, refresh_token: str) -> dict[str, str]:
        """Validate refresh token and return a new access+refresh token pair."""

        token_payload_dto: JwtPayloadDto = (
            self._jwt_service.verify_refresh_token(refresh_token)
        )

        user_persistence_dto: PersistenceUserDto | None = (
            self._user_repo.get_user_by_id(UUID(token_payload_dto.sub))
        )
        if user_persistence_dto is None:
            raise ValueError("UserEntity not found")

        user: UserEntity = UserMapper.to_entity_from_persistence(
            user_persistence_dto
        )

        return self._generate_jwt_tokens(user)

    def verify_jwt_token(
        self, token: str, subject: str | None = None
    ) -> JwtPayloadDto:
        jwt_token_payload_dto: JwtPayloadDto = self._jwt_service.verify(
            token, subject
        )
        return jwt_token_payload_dto

    def logout(self, token: str) -> None:
        jwt_token_payload_dto: JwtPayloadDto = self._jwt_service.verify(token)
        jti: str = jwt_token_payload_dto.jti
        exp: float = jwt_token_payload_dto.exp

        expires_in: float = exp - utc_now_time_stamp()
        expires_at: datetime = utc_now() + timedelta(seconds=expires_in)

        self._jwt_repo.add_token(jti=jti, expires_at=expires_at)
