from application.dto.auth.jwt.tokens import JwtTokensDto
from domain.entities.user import UserEntity
from domain.services.auth.authenticate.authenticate_user import AuthenticateUser
from domain.services.auth.jwt.issue_jwt import IssueJwt
from domain.value_objects.email import EmailVo


class JwtLoginUserUseCase:
    """Authenticate a user and issue JWTs."""

    def __init__(
        self, authenticate_user: AuthenticateUser, issue_jwt: IssueJwt
    ):
        self._authenticate_user = authenticate_user
        self._issue_jwt = issue_jwt

    async def execute(self, email: str, password: str) -> JwtTokensDto:
        email_vo = EmailVo.from_string(email)
        user: UserEntity = await self._authenticate_user.authenticate_user(
            email_vo, password
        )
        access_token: str = self._issue_jwt.issue_access_token(user)
        refresh_token: str = self._issue_jwt.issue_refresh_token(user)
        return JwtTokensDto(
            access_token=access_token, refresh_token=refresh_token
        )
