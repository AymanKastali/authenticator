from application.dto.user_dto import UserDto
from application.mappers.user_mapper import UserMapper
from application.ports.user_repository import UserRepositoryPort
from application.services.password_service import PasswordService
from domain.entities.user import User
from domain.exceptions.domain_exceptions import InvalidValueError
from domain.value_objects.email import Email
from domain.value_objects.hashed_password import HashedPassword


class RegisterUserUseCase:
    def __init__(
        self, user_repo: UserRepositoryPort, password_service: PasswordService
    ):
        self._user_repo = user_repo
        self._password_service = password_service

    def _validate_email(self, email: str) -> Email:
        try:
            return Email.from_string(email)
        except InvalidValueError as e:
            raise ValueError(f"Invalid email: {e}") from e

    def _ensure_email_available(self, email: str) -> None:
        if self._user_repo.get_user_by_email(email):
            raise ValueError(f"Email '{email}' is already registered.")

    def _create_user(
        self, email_vo: Email, hashed_password: HashedPassword
    ) -> User:
        return User.register_local(
            email=email_vo, hashed_password=hashed_password
        )

    def execute(self, email: str, password: str) -> UserDto:
        self._ensure_email_available(email)
        email_vo = self._validate_email(email)

        hashed_password = self._password_service.create_hashed_password(
            password
        )

        user = self._create_user(email_vo, hashed_password)

        self._user_repo.save(UserMapper.to_persistence_dto_from_entity(user))

        return UserMapper.to_user_dto_from_entity(user)
