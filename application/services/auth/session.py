from application.dto.auth.session.persistence import PersistenceSessionDto
from domain.entities.session import SessionEntity
from domain.ports.repositories.session import SessionRepositoryPort
from domain.services.user import UserDomainService
from domain.value_objects.email import EmailVo


class SessionAuthService:
    def __init__(
        self,
        user_service: UserDomainService,
        session_repo: SessionRepositoryPort,
    ):
        self._user_service = user_service
        self._session_repo = session_repo

    async def _authenticate_user_local(self, email: str, password: str):
        """Authenticate a user using local credentials."""

        email_vo = EmailVo.from_string(email)
        user = await self._user_service.authenticate_user(email_vo, password)

        return user

    async def create_session(self, email: str, password: str) -> str:
        user = await self._authenticate_user_local(email, password)

        if not user:
            raise ValueError("Invalid credentials")

        # Create a new session entity
        session = SessionEntity.create(user_id=user.uid)

        # Convert to persistence DTO
        session_dto = PersistenceSessionDto(
            session_id=session.uid.value, user_id=user.uid.to_string()
        )

        # Save session to repository
        created_session = self._session_repo.create_session(session_dto)

        return created_session.session_id
