from application.dto.user_dto import UserDTO
from application.ports.user_repository import UserRepositoryPort
from domain.entities.user import User
from domain.value_objects.email_address import EmailAddress


class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def execute(self, email_address: str, password: str) -> UserDTO:
        user: User = User.register_local(
            email_address=EmailAddress(email_address),
            password=password,
        )
        self.user_repo.save(user)
        return UserDTO.from_entity(user)
