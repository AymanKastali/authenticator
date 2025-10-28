from application.dto.session import PersistenceSessionDto
from application.dto.user_dto import PersistenceUserDto
from application.mappers.user_mapper import UserMapper
from application.ports.session_repository import SessionRepositoryPort
from application.ports.user_repository import UserRepositoryPort
from domain.entities.session import Session


class SessionAuthService:
    def __init__(
        self, user_repo: UserRepositoryPort, session_repo: SessionRepositoryPort
    ):
        self._user_repo = user_repo
        self.session_repo = session_repo

    def _authenticate_user_local(
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

    def create_session(self, email: str, password: str) -> str:
        user_dto: PersistenceUserDto | None = self._authenticate_user_local(
            email, password
        )
        if not user_dto:
            return None

        user = UserMapper.to_entity_from_persistence(user_dto)

        session: Session = Session.create(user_id=user.uid)
        session_dto = PersistenceSessionDto(
            session_id=session.uid.value, user_id=user.uid.to_string()
        )
        created_session = self.session_repo.create_session(session_dto)
        return created_session.session_id
