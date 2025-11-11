from fastapi import Depends

from application.use_cases.auth.registration.register import RegisterUserUseCase
from domain.services.user.register_user import RegisterUser
from presentation.web.fastapi.api.v1.dependencies.domain.user import (
    register_user_dependency,
)


# Use Cases
def register_user_uc_dependency(
    registration: RegisterUser = Depends(register_user_dependency),
) -> RegisterUserUseCase:
    """Provide use case for registering a user"""
    return RegisterUserUseCase(registration)
