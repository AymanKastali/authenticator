from application.dto.auth.jwt.tokens import JwtTokensDto
from application.use_cases.auth.authenticate_user import (
    AuthenticateUserUseCase,
)
from application.use_cases.jwt.issue_jwt import IssueJwtUseCase
from domain.entities.user import UserEntity
from domain.factories.value_objects.email import EmailVoFactory


class JwtLoginUserService:
    """Authenticate a user and issue JWTs."""

    def __init__(
        self,
        authenticate_user: AuthenticateUserUseCase,
        issue_jwt: IssueJwtUseCase,
    ):
        self._authenticate_user = authenticate_user
        self._issue_jwt = issue_jwt

    async def execute(self, email: str, password: str) -> JwtTokensDto:
        email_vo = EmailVoFactory.from_string(email)
        user: UserEntity = await self._authenticate_user.authenticate_user(
            email=email_vo, raw_password=password
        )
        access_token: str = self._issue_jwt.issue_access_token(user)
        refresh_token: str = self._issue_jwt.issue_refresh_token(user)
        return JwtTokensDto(
            access_token=access_token, refresh_token=refresh_token
        )
