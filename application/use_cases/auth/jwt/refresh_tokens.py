from application.dto.auth.jwt.tokens import JwtTokensDto
from domain.entities.auth.jwt.token import JwtEntity
from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import UserNotFoundError
from domain.services.jwt.issue_jwt import IssueJwt
from domain.services.jwt.validate_jwt import ValidateJwt
from domain.services.user.query_user import QueryUser
from domain.value_objects.jwt_payload import JwtPayloadVo


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
        payload_vo: JwtPayloadVo = self._validate_jwt.refresh(refresh_token)
        user: UserEntity | None = await self._query_user.get_user_by_id(
            payload_vo.sub
        )
        if user is None:
            raise UserNotFoundError(payload_vo.sub.to_string())

        access_token: JwtEntity = self._issue_jwt.access(user)
        refresh_token_entity: JwtEntity = self._issue_jwt.refresh(user)
        return JwtTokensDto(
            access_token=access_token.signature,
            refresh_token=refresh_token_entity.signature,
        )
