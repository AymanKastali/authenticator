from application.dto.auth.jwt.token_user import TokenUserDto
from application.mappers.user import UserMapper
from application.services.jwt.jwt_blacklist import JwtBlacklistService
from application.services.user import UserQueryService
from application.use_cases.jwt.validate_jwt import ValidateJwtUseCase
from domain.entities.jwt_token import JwtEntity
from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import UserNotFoundError


class GetJwtAuthenticatedUserService:
    def __init__(
        self,
        validate_jwt: ValidateJwtUseCase,
        blacklist_service: JwtBlacklistService,
        user_query_service: UserQueryService,
    ):
        self._validate_jwt = validate_jwt
        self._blacklist_service = blacklist_service
        self._user_query_service = user_query_service

    async def execute(self, token: str) -> TokenUserDto:
        token_entity: JwtEntity = self._validate_jwt.execute(
            token=token, token_type="access"
        )

        await self._blacklist_service.assert_not_blacklisted(
            token_entity.uid.value
        )

        user: UserEntity | None = await self._user_query_service.get_user_by_id(
            token_entity.subject
        )
        if user is None:
            raise UserNotFoundError(token_entity.subject.value)

        return UserMapper.to_token_dto(user)
