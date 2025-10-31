from datetime import datetime, timedelta
from uuid import UUID

from application.dto.auth.jwt.token import JwtDto
from application.dto.user.persistence import PersistenceUserDto
from application.mappers.jwt import JwtMapper
from application.mappers.user import UserMapper
from application.ports.repositories.jwt import JwtRepositoryPort
from application.ports.repositories.user import UserRepositoryPort
from application.ports.services.jwt import JwtServicePort
from domain.entities.auth.jwt.token import JwtEntity
from domain.entities.user import UserEntity
from domain.utils.time import expires_after, utc_now, utc_now_time_stamp
from domain.value_objects.jwt_payload import JwtPayloadVo
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

    def _create_access_token(self, user: UserEntity) -> JwtEntity:
        payload_vo = JwtPayloadVo.create(
            sub=user.uid,
            email=user.email,
            typ=JwtTokenType.ACCESS,
            roles=list(user.roles),
            exp=expires_after(minutes=30),
        )
        payload_dto = JwtMapper.to_payload_dto_from_vo(payload_vo)
        jwt_dto = self._jwt_service.sign(payload_dto)
        jwt_entity = JwtEntity.create_signed(
            payload=payload_vo, signature=jwt_dto.signature
        )
        return jwt_entity

    def _create_refresh_token(self, user: UserEntity) -> JwtEntity:
        payload_vo = JwtPayloadVo.create(
            sub=user.uid,
            email=user.email,
            typ=JwtTokenType.REFRESH,
            roles=list(user.roles),
            exp=expires_after(days=7),
        )
        payload_dto = JwtMapper.to_payload_dto_from_vo(payload_vo)
        jwt_dto = self._jwt_service.sign(payload_dto)
        jwt_entity = JwtEntity.create_signed(
            payload=payload_vo, signature=jwt_dto.signature
        )
        return jwt_entity

    def _generate_jwt_tokens(self, user: UserEntity) -> dict[str, str]:
        return {
            "access_token": self._create_access_token(user).signature,
            "refresh_token": self._create_refresh_token(user).signature,
        }

    def login_user(self, email: str, password: str) -> dict[str, str]:
        """Authenticate and return JWT tokens."""
        user_dto = self._authenticate_user_local(email, password)
        user_entity = UserMapper.to_entity_from_persistence(user_dto)
        return self._generate_jwt_tokens(user_entity)

    def refresh_jwt_token(self, refresh_token: str) -> dict[str, str]:
        """Validate refresh token and return a new access+refresh token pair."""

        token_dto: JwtDto = self._jwt_service.verify_refresh_token(
            refresh_token
        )

        user_persistence_dto: PersistenceUserDto | None = (
            self._user_repo.get_user_by_id(UUID(token_dto.payload.sub))
        )
        if user_persistence_dto is None:
            raise ValueError("UserEntity not found")

        user: UserEntity = UserMapper.to_entity_from_persistence(
            user_persistence_dto
        )

        return self._generate_jwt_tokens(user)

    def verify_jwt_token(
        self, token: str, subject: str | None = None
    ) -> JwtDto:
        token_dto: JwtDto = self._jwt_service.verify(token, subject)
        return token_dto

    def logout(self, token: str) -> None:
        token_dto: JwtDto = self._jwt_service.verify(token)
        jti: str = token_dto.payload.jti
        exp: float = token_dto.payload.exp

        expires_in: float = exp - utc_now_time_stamp()
        expires_at: datetime = utc_now() + timedelta(seconds=expires_in)

        self._jwt_repo.add_token(jti=jti, expires_at=expires_at)

    def is_token_valid(self, token: str) -> bool:
        """Check signature, expiration, and blacklist."""
        # 1️⃣ Verify token → get DTO
        token_dto: JwtDto = self._jwt_service.verify(token)

        # 2️⃣ Convert DTO → domain VO
        payload_vo = JwtMapper.to_payload_vo_from_dto(token_dto.payload)

        # 3️⃣ Use domain behavior
        if payload_vo.is_expired():
            return False

        if self._jwt_repo.is_token_blacklisted(payload_vo.jti.to_string()):
            return False

        return True
