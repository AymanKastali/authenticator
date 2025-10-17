from adapters.gateways.authentication.jwt_service import JwtService
from adapters.gateways.persistence.in_memory.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)
from application.use_cases.login_user import LoginUserUseCase
from domain.entities.user import User
from domain.services.authentication import AuthenticationService
from domain.value_objects.email_address import EmailAddress

# Setup
user_repo = InMemoryUserRepository()
jwt_service = JwtService(secret="supersecretkey")
auth_service = AuthenticationService(user_repo)
login_use_case = LoginUserUseCase(auth_service, jwt_service)

# Create a user
user = User.register_local(
    EmailAddress("alice@example.com"), "strongpassword123"
)
user_repo.save(user)

# Attempt login
result = login_use_case.execute("alice@example.com", "strongpassword123")
if result:
    print("✅ Login successful!")
    print(result)
else:
    print("❌ Invalid credentials")
