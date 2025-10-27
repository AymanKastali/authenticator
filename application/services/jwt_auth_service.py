from application.dto.user_dto import PersistenceUserDto
from application.mappers.jwt_mapper import JwtTokenPayloadMapper
from application.mappers.user_mapper import UserMapper
from application.ports.jwt_token_service_port import JwtTokenServicePort
from application.ports.user_repository import UserRepositoryPort
from domain.entities.jwt_token_payload import JwtTokenPayload
from domain.entities.user import User
from domain.utils.date_time_utils import expires_after
from domain.value_objects.jwt_token_type import JwtTokenType


class JwtAuthService:
    def __init__(
        self,
        user_repo: UserRepositoryPort,
        jwt_service: JwtTokenServicePort,
    ):
        self._user_repo = user_repo
        self._jwt_service = jwt_service

    def _authenticate_user_local(
        self, email: str, password: str
    ) -> PersistenceUserDto:
        """Authenticate a user using local credentials."""
        user_dto = self._user_repo.get_user_by_email(email)
        if user_dto is None:
            raise ValueError("User not found")

        user_entity = UserMapper.to_entity_from_persistence(user_dto)

        # ✅ Corrected logic — reject inactive or invalid password
        if not user_entity.active:
            raise ValueError("User account is inactive")

        if not user_entity.verify_password(password):
            raise ValueError("Invalid credentials")

        return user_dto

    def generate_access_token(self, user: User) -> str:
        payload = JwtTokenPayload.create(
            sub=user.uid,
            email=user.email,
            typ=JwtTokenType.ACCESS,
            roles=list(user.roles),
            exp=expires_after(minutes=30),
        )
        payload_dto = JwtTokenPayloadMapper.to_dto_from_entity(payload)
        return self._jwt_service.sign(payload_dto)

    def generate_refresh_token(self, user: User) -> str:
        payload = JwtTokenPayload.create(
            sub=user.uid,
            email=user.email,
            typ=JwtTokenType.REFRESH,
            roles=list(user.roles),
            exp=expires_after(days=7),
        )
        payload_dto = JwtTokenPayloadMapper.to_dto_from_entity(payload)
        return self._jwt_service.sign(payload_dto)

    def generate_jwt_tokens(self, user: User) -> dict[str, str]:
        return {
            "access_token": self.generate_access_token(user),
            "refresh_token": self.generate_refresh_token(user),
        }

    def execute(self, email: str, password: str) -> dict[str, str]:
        """Authenticate and return JWT tokens."""
        user_dto = self._authenticate_user_local(email, password)
        user_entity = UserMapper.to_entity_from_persistence(user_dto)
        return self.generate_jwt_tokens(user_entity)
