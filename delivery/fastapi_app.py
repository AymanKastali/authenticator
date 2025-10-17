from fastapi import FastAPI

from adapters.controllers.auth_controller import AuthController
from adapters.gateways.authentication.jwt_service import JwtService
from adapters.gateways.persistence.in_memory.repositories.in_memory_user_repository import (
    InMemoryUserRepository,
)
from application.use_cases.login_user import LoginUserUseCase
from domain.entities.user import User
from domain.services.authentication import AuthenticationService
from domain.value_objects.email_address import EmailAddress

# ---------- Setup infrastructure ----------
user_repo = InMemoryUserRepository()
jwt_service = JwtService(secret="supersecret", expiration_minutes=60)

# Create a demo user
demo_user = User.register_local(
    email=EmailAddress("demo@example.com"), password="password123"
)
user_repo.save(demo_user)

# ---------- Setup use case ----------
auth_service = AuthenticationService(user_repository=user_repo)
login_use_case = LoginUserUseCase(
    auth_service=auth_service, jwt_service=jwt_service
)

# For demonstration, we manually inject AuthenticationService here

auth_service = AuthenticationService(user_repository=user_repo)
login_use_case.auth_service = auth_service

# ---------- Setup controller ----------
auth_controller = AuthController(login_use_case=login_use_case)

# ---------- FastAPI app ----------
app = FastAPI(title="Authentication Microservice")


@app.post("/login")
def login_handler(payload: dict):
    email = payload.get("email")
    password = payload.get("password")
    if email is None or password is None:
        raise ValueError("Email and password are required")
    return auth_controller.login(email, password)
