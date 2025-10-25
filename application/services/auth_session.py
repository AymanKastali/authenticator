from application.ports.session_repository import SessionRepositoryPort
from application.ports.user_repository import UserRepositoryPort
from domain.entities.user import User


class SessionAuthService:
    def __init__(
        self, user_repo: UserRepositoryPort, session_repo: SessionRepositoryPort
    ):
        self.user_repo = user_repo
        self.session_repo = session_repo

    def authenticate_local(self, email: str, password: str) -> User | None:
        user = self.user_repo.get_user_by_email(email)
        if not user or not user.active or not user.verify_password(password):
            return None
        return user

    def create_session(self, user: User, data: dict | None = None) -> str:
        session = self.session_repo.create_session(user.uid, data)
        return session.uid.value
