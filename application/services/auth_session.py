from application.dto.user_dto import PersistenceUserDto
from application.mappers.user_mapper import UserMapper
from application.ports.session_repository import SessionRepositoryPort
from application.ports.user_repository import UserRepositoryPort
from domain.entities.user import User


class SessionAuthService:
    def __init__(
        self, user_repo: UserRepositoryPort, session_repo: SessionRepositoryPort
    ):
        self._user_repo = user_repo
        self.session_repo = session_repo

    def authenticate_user_local(
        self, email: str, password: str
    ) -> PersistenceUserDto:
        """Authenticate a user using local credentials."""
        user_dto = self._user_repo.get_user_by_email(email)
        if user_dto is None:
            raise ValueError("User not found")

        user_entity = UserMapper.to_entity_from_persistence(user_dto)

        if not user_entity.active:
            raise ValueError("User account is inactive")

        if not user_entity.verify_password(password):
            raise ValueError("Invalid credentials")

        return user_dto

    def create_session(self, user: User, data: dict | None = None) -> str:
        session = self.session_repo.create_session(user.uid, data)
        return session.uid.value
