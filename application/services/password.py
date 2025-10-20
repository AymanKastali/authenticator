from domain.entities.user import User


class PasswordService:
    """Domain rules around passwords."""

    @staticmethod
    def validate_strength(password: str) -> bool:
        return len(password) >= 8 and any(c.isdigit() for c in password)

    @staticmethod
    def change_password(user: User, new_password: str):
        if not PasswordService.validate_strength(new_password):
            raise ValueError("Password does not meet policy")
        user.change_password(new_password)
