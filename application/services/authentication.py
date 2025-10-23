from application.ports.user_repository import UserRepositoryPort
from domain.entities.user import User
from domain.value_objects.email import Email


class AuthenticationService:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def authenticate_local(self, email: Email, password: str) -> User | None:
        user = self.user_repo.get_user_by_email(email)
        if not user or not user.active or not user.verify_password(password):
            return None
        return user
