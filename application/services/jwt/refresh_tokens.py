from application.dto.auth.jwt.tokens import JwtTokensDto
from application.use_cases.jwt.issue_jwt import IssueJwtUseCase
from application.use_cases.jwt.validate_jwt import ValidateJwtUseCase
from domain.entities.jwt_token import JwtEntity
from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import UserNotFoundError
from domain.ports.repositories.user import UserRepositoryPort


class RefreshJwtTokensService:
    """Validate refresh token and issue new JWT pair."""

    def __init__(
        self,
        validate_jwt: ValidateJwtUseCase,
        issue_jwt: IssueJwtUseCase,
        user_repo: UserRepositoryPort,
    ):
        self._validate_jwt = validate_jwt
        self._issue_jwt = issue_jwt
        self._user_repo = user_repo

    async def execute(self, refresh_token: str) -> JwtTokensDto:
        token_entity: JwtEntity = self._validate_jwt.execute(
            token=refresh_token, token_type="refresh"
        )
        user: UserEntity | None = await self._user_repo.get_user_by_id(
            token_entity.subject
        )
        if user is None:
            raise UserNotFoundError(token_entity.subject.value)

        access_token: str = self._issue_jwt.issue_access_token(user)
        refresh_token = self._issue_jwt.issue_refresh_token(user)
        return JwtTokensDto(
            access_token=access_token, refresh_token=refresh_token
        )
