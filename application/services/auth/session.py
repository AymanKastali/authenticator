from application.dto.auth.session.persistence import PersistenceSessionDto
from application.dto.user.persistence import PersistenceUserDto
from application.mappers.user import UserMapper
from application.ports.repositories.session import SessionRepositoryPort
from application.ports.repositories.user import UserRepositoryPort
from domain.entities.auth.session.session import SessionEntity


class SessionAuthService:
    def __init__(
        self, user_repo: UserRepositoryPort, session_repo: SessionRepositoryPort
    ):
        self._user_repo = user_repo
        self.session_repo = session_repo

    async def _authenticate_user_local(
        self, email: str, password: str
    ) -> PersistenceUserDto:
        """Authenticate a user using local credentials."""
        user_dto = await self._user_repo.get_user_by_email(email)
        if user_dto is None:
            raise ValueError("UserEntity not found")

        user_entity = UserMapper.to_entity_from_persistence(user_dto)

        if not user_entity.active:
            raise ValueError("UserEntity account is inactive")

        if not user_entity.verify_password(password):
            raise ValueError("Invalid credentials")

        return user_dto

    async def create_session(self, email: str, password: str) -> str:
        user_dto: (
            PersistenceUserDto | None
        ) = await self._authenticate_user_local(email, password)
        if not user_dto:
            return None

        user = UserMapper.to_entity_from_persistence(user_dto)

        session: SessionEntity = SessionEntity.create(user_id=user.uid)
        session_dto = PersistenceSessionDto(
            session_id=session.uid.value, user_id=user.uid.to_string()
        )
        created_session = self.session_repo.create_session(session_dto)
        return created_session.session_id
