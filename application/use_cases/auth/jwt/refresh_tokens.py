from application.dto.auth.jwt.tokens import JwtTokensDto
from domain.entities.jwt_token import JwtEntity
from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import UserNotFoundError
from domain.services.auth.jwt.issue_jwt import IssueJwt
from domain.services.auth.jwt.validate_jwt import ValidateJwt
from domain.services.user.query_user import QueryUser


class RefreshTokensUseCase:
    """Validate refresh token and issue new JWT pair."""

    def __init__(
        self,
        validate_jwt: ValidateJwt,
        issue_jwt: IssueJwt,
        query_user: QueryUser,
    ):
        self._validate_jwt = validate_jwt
        self._issue_jwt = issue_jwt
        self._query_user = query_user

    async def execute(self, refresh_token: str) -> JwtTokensDto:
        token_entity: JwtEntity = self._validate_jwt.validate_refresh_token(
            refresh_token
        )
        user: UserEntity | None = await self._query_user.get_user_by_id(
            token_entity.subject
        )
        if user is None:
            raise UserNotFoundError(token_entity.subject.to_string())

        access_token: str = self._issue_jwt.issue_access_token(user)
        refresh_token = self._issue_jwt.issue_refresh_token(user)
        return JwtTokensDto(
            access_token=access_token, refresh_token=refresh_token
        )
