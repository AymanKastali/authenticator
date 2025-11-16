from application.dto.auth.jwt.token_user import TokenUserDto
from application.mappers.user import UserMapper
from application.repositories.user import UserRepository
from application.use_cases.jwt.assert_jwt_revocation import (
    AssertJwtRevocationUseCase,
)
from application.use_cases.jwt.validate_jwt import ValidateJwtUseCase
from domain.entities.jwt_token import JwtEntity
from domain.entities.user import UserEntity
from domain.exceptions.domain_errors import UserNotFoundError


class GetJwtAuthenticatedUserService:
    def __init__(
        self,
        validate_jwt: ValidateJwtUseCase,
        assert_jwt_revocation: AssertJwtRevocationUseCase,
        user_repo: UserRepository,
    ):
        self._validate_jwt = validate_jwt
        self._assert_jwt_revocation = assert_jwt_revocation
        self._user_repo = user_repo

    async def execute(self, token: str) -> TokenUserDto:
        token_entity: JwtEntity = self._validate_jwt.validate_access_token(
            token
        )

        await self._assert_jwt_revocation.execute(token_entity.uid)

        user: UserEntity | None = await self._user_repo.get_user_by_id(
            token_entity.subject
        )
        if user is None:
            raise UserNotFoundError(token_entity.subject.value)

        return UserMapper.to_token_dto(user)
