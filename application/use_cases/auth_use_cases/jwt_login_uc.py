# from application.ports.user_repository import UserRepositoryPort
# from application.services.jwt_auth_service import JwtAuthService
# from domain.entities.user import User
# from domain.value_objects.email import Email
# from domain.value_objects.jwt_payload import JwtTokenPayload


# class JwtLoginUseCase:
#     def __init__(
#         self, user_repo: UserRepositoryPort, jwt_auth_service: JwtAuthService
#     ):
#         self.user_repo = user_repo
#         self.jwt_auth_service = jwt_auth_service

#     def _authenticate_local(self, email: Email, password: str) -> User | None:
#         user = self.user_repo.get_user_by_email(email)
#         if not user or not user.active or not user.verify_password(password):
#             return None
#         return user

#     def execute(self, email: str, password: str) -> dict:
#         user: User | None = self._authenticate_local(
#             Email.from_string(email), password
#         )
#         if not user:
#             raise ValueError("Invalid credentials")

#         # claims: JwtClaims = JwtClaims(
#         #     roles=[role.value for role in user.roles], email=user.email.value
#         # )
#         payload: JwtTokenPayload = JwtTokenPayload().build(
#             email=user.email.value, roles=[role.value for role in user.roles]
#         )

#         tokens: dict = self.jwt_auth_service.generate_jwt_tokens(payload)
#         raw_tokens: dict = {
#             "access_token": tokens["access_token"].get_value(),
#             "refresh_token": tokens["refresh_token"].get_value(),
#         }
#         return raw_tokens
