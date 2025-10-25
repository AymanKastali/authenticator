from application.dto.user_dto import PersistenceUserDto
from application.mappers.jwt_mapper import JwtTokenPayloadMapper
from application.mappers.user_mapper import UserMapper
from application.ports.jwt_token_service_port import JwtTokenServicePort
from application.ports.user_repository import UserRepositoryPort

# from domain.entities.user import User
from domain.entities.jwt_token_payload import JwtTokenPayload
from domain.entities.user import User
from domain.utils.date_time_utils import (
    expires_after_days,
    expires_after_minutes,
)
from domain.value_objects.jwt_token_type import JwtTokenType


class JwtAuthService:
    def __init__(
        self, user_repo: UserRepositoryPort, jwt_service: JwtTokenServicePort
    ):
        self.user_repo = user_repo
        self.jwt_service = jwt_service

    def _authenticate_user_local(
        self, email: str, password: str
    ) -> PersistenceUserDto:
        user: PersistenceUserDto | None = self.user_repo.get_user_by_email(
            email
        )

        if user is None:
            raise ValueError("User Not Found")

        user_entity: User = UserMapper.to_entity_from_persistence(user)
        if not user.active or user_entity.verify_password(password):
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
        payload_dto = JwtTokenPayloadMapper.to_dto_from_entity(payload)
        access_token: str = self.jwt_service.sign(payload_dto)
        return access_token

    def generate_refresh_token(self, user: User) -> str:
        payload = JwtTokenPayload.create(
            sub=user.uid,
            email=user.email,
            typ=JwtTokenType.REFRESH,
            roles=list(user.roles),
            exp=expires_after_days(7),
        )
        payload_dto = JwtTokenPayloadMapper.to_dto_from_entity(payload)
        refresh_token: str = self.jwt_service.sign(payload_dto)
        return refresh_token

    def generate_jwt_tokens(self, user: User) -> dict[str, str]:
        at = self.generate_access_token(user)
        rt = self.generate_refresh_token(user)
        return {"access_token": at, "refresh_token": rt}

    def execute(self, email: str, password: str):
        user: PersistenceUserDto = self._authenticate_user_local(
            email=email, password=password
        )
        user_entity: User = UserMapper.to_entity_from_persistence(user)
        return self.generate_jwt_tokens(user_entity)
