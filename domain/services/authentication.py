from domain.entities.user import User
from domain.interfaces.user import IUserRepository
from domain.value_objects.email_address import EmailAddress


class AuthenticationService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def authenticate_local(
        self, email: EmailAddress, password: str
    ) -> User | None:
        user = self.user_repository.find_by_email(email)
        if not user or not user.is_active or not user.verify_password(password):
            return None
        return user
