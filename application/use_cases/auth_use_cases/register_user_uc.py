from application.dto.user_dto.user_dto import UserDTO
from application.ports.user_repository import UserRepositoryPort
from domain.config.config_models import PasswordConfig
from domain.entities.user import User
from domain.value_objects.email import EmailAddress


class RegisterUserUseCase:
    def __init__(
        self, user_repo: UserRepositoryPort, password_cfg: PasswordConfig
    ):
        self.user_repo = user_repo
        self.password_cfg = password_cfg

    def execute(self, email: str, password: str) -> UserDTO:
        user: User = User.register_local(
            email=EmailAddress(email),
            password=password,
            password_cfg=self.password_cfg,
        )
        self.user_repo.save(user)
        return UserDTO.from_entity(user)
