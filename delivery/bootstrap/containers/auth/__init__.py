from .jwt import JwtAuthContainer
from .registration import RegistrationContainer
from .session import SessionAuthContainer

jwt_auth_container = JwtAuthContainer()
session_auth_container = SessionAuthContainer()
registration_container = RegistrationContainer()
