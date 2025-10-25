from application.dto.user_dto import PersistenceUserDto, UserDto
from application.mappers.user_mapper import UserMapper
from application.ports.user_repository import UserRepositoryPort
from domain.config.config_models import PasswordConfig
from domain.entities.user import User
from domain.exceptions.domain_exceptions import InvalidValueError
from domain.value_objects.email import Email


class RegisterUserUseCase:
    def __init__(
        self, user_repo: UserRepositoryPort, password_cfg: PasswordConfig
    ):
        self.user_repo = user_repo
        self.password_cfg = password_cfg

    def _validate_email(self, email: str) -> Email:
        try:
            return Email.from_string(email)
        except InvalidValueError as e:
            raise ValueError(f"Invalid email: {e}") from e

    def _ensure_email_available(self, email: str) -> None:
        if self.user_repo.get_user_by_email(email):
            raise ValueError(f"Email '{email}' is already registered.")

    def _create_user(self, email_vo: Email, password: str) -> User:
        return User.register_local(
            email=email_vo, password=password, password_cfg=self.password_cfg
        )

    def _save_user(self, user: PersistenceUserDto) -> None:
        self.user_repo.save(user)

    def _to_dto(self, user: User) -> UserDto:
        return UserMapper.to_user_dto(user)

    def execute(self, email: str, password: str) -> UserDto:
        self._ensure_email_available(email)
        email_vo: Email = self._validate_email(email)
        user: User = self._create_user(email_vo, password)
        self._save_user(UserMapper.to_persistence_dto(user))
        return self._to_dto(user)
