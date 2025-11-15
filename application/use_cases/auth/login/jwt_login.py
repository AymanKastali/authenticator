from application.dto.auth.jwt.tokens import JwtTokensDto
from domain.entities.user import UserEntity
from domain.factories.value_objects.email import EmailVoFactory
from domain.services.auth.authenticate.authenticate_user import AuthenticateUser
from domain.services.auth.jwt.issue_jwt import IssueJwt


class JwtLoginUserUseCase:
    """Authenticate a user and issue JWTs."""

    def __init__(
        self, authenticate_user: AuthenticateUser, issue_jwt: IssueJwt
    ):
        self._authenticate_user = authenticate_user
        self._issue_jwt = issue_jwt

    async def execute(self, email: str, password: str) -> JwtTokensDto:
        email_vo = EmailVoFactory.from_string(email)
        user: UserEntity = await self._authenticate_user.authenticate_user(
            email=email_vo, raw_password=password
        )
        print("user: ", user)
        access_token: str = self._issue_jwt.issue_access_token(user)
        print("access_token: ", access_token)
        refresh_token: str = self._issue_jwt.issue_refresh_token(user)
        return JwtTokensDto(
            access_token=access_token, refresh_token=refresh_token
        )
