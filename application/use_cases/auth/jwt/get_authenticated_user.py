from application.dto.auth.jwt.token_user import TokenUserDto
from application.mappers.user import UserMapper
from domain.entities.auth.jwt.token import JwtEntity
from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import UserNotFoundError
from domain.services.jwt.revoke_jwt import RevokeJwt
from domain.services.jwt.validate_jwt import ValidateJwt
from domain.services.user.query_user import QueryUser


class GetAuthenticatedUserUseCase:
    def __init__(
        self,
        validate_jwt: ValidateJwt,
        revoke_jwt: RevokeJwt,
        query_user: QueryUser,
    ):
        self._validate_jwt = validate_jwt
        self._revoke_jwt = revoke_jwt
        self._query_user = query_user

    async def execute(self, token: str) -> TokenUserDto:
        token_entity: JwtEntity = self._validate_jwt.validate_access_token(
            token
        )

        await self._revoke_jwt.assert_not_revoked(token_entity.uid)

        user: UserEntity | None = await self._query_user.get_user_by_id(
            token_entity.subject
        )
        if user is None:
            raise UserNotFoundError(token_entity.subject.to_string())

        return UserMapper.to_token_user_dto_from_entity(user)
