from application.dto.user_dto.user_dto import UserDTO
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

    def _ensure_email_available(self, email_vo: Email) -> None:
        if self.user_repo.get_user_by_email(email_vo):
            raise ValueError(f"Email '{email_vo.value}' is already registered.")

    def _create_user(self, email_vo: Email, password: str) -> User:
        return User.register_local(
            email=email_vo, password=password, password_cfg=self.password_cfg
        )

    def _save_user(self, user: User) -> None:
        self.user_repo.save(user)

    def _to_dto(self, user: User) -> UserDTO:
        return UserDTO.from_entity(user)

    def execute(self, email: str, password: str) -> UserDTO:
        email_vo: Email = self._validate_email(email)
        self._ensure_email_available(email_vo)
        user: User = self._create_user(email_vo, password)
        self._save_user(user)
        return self._to_dto(user)
