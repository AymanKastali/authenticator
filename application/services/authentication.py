from application.mappers.user_mapper import UserMapper
from application.ports.user_repository import UserRepositoryPort
from domain.entities.user import User


class AuthenticationService:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def authenticate_local(self, email: str, password: str) -> User | None:
        user = self.user_repo.get_user_by_email(email)
        if (
            not user
            or not user.active
            or not UserMapper.to_entity_from_persistence(user).verify_password(
                password
            )
        ):
            return None
        return user
