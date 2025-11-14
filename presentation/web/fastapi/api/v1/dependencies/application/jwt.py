from fastapi import Depends

from application.use_cases.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserUseCase,
)
from application.use_cases.auth.jwt.logout import LogoutUserUseCase
from application.use_cases.auth.jwt.refresh_tokens import RefreshTokensUseCase
from application.use_cases.auth.jwt.verify_access_token import (
    VerifyAccessTokenUseCase,
)
from application.use_cases.auth.jwt.verify_refresh_token import (
    VerifyRefreshTokenUseCase,
)
from application.use_cases.auth.login.jwt_login import JwtLoginUserUseCase
from domain.services.auth.authenticate.authenticate_user import AuthenticateUser
from domain.services.auth.jwt.issue_jwt import IssueJwt
from domain.services.auth.jwt.revoke_jwt import RevokeJwt
from domain.services.auth.jwt.validate_jwt import ValidateJwt
from presentation.web.fastapi.api.v1.dependencies.domain.authentication import (
    authenticate_user_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.domain.jwt import (
    jwt_issuance_dependency,
    jwt_revocation_dependency,
    jwt_validation_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.domain.user import (
    query_user_dependency,
)


# Use Cases
def get_authenticated_user_uc_dependency(
    validate_jwt: ValidateJwt = Depends(jwt_validation_dependency),
    revoke_jwt: RevokeJwt = Depends(jwt_revocation_dependency),
    query_user=Depends(query_user_dependency),
) -> GetAuthenticatedUserUseCase:
    return GetAuthenticatedUserUseCase(
        validate_jwt=validate_jwt, revoke_jwt=revoke_jwt, query_user=query_user
    )


def jwt_login_user_uc_dependency(
    authenticate_user: AuthenticateUser = Depends(authenticate_user_dependency),
    issue_jwt: IssueJwt = Depends(jwt_issuance_dependency),
) -> JwtLoginUserUseCase:
    return JwtLoginUserUseCase(
        authenticate_user=authenticate_user, issue_jwt=issue_jwt
    )


def jwt_logout_user_uc_dependency(
    validate_jwt: ValidateJwt = Depends(jwt_validation_dependency),
    revoke_jwt: RevokeJwt = Depends(jwt_revocation_dependency),
) -> LogoutUserUseCase:
    return LogoutUserUseCase(validate_jwt=validate_jwt, revoke_jwt=revoke_jwt)


def jwt_refresh_tokens_uc_dependency(
    validate_jwt: ValidateJwt = Depends(jwt_validation_dependency),
    issue_jwt: IssueJwt = Depends(jwt_issuance_dependency),
    query_user=Depends(query_user_dependency),
) -> RefreshTokensUseCase:
    return RefreshTokensUseCase(
        query_user=query_user, issue_jwt=issue_jwt, validate_jwt=validate_jwt
    )


def jwt_verify_access_token_uc_dependency(
    validate_jwt: ValidateJwt = Depends(jwt_validation_dependency),
    revoke_jwt: RevokeJwt = Depends(jwt_revocation_dependency),
) -> VerifyAccessTokenUseCase:
    return VerifyAccessTokenUseCase(
        validate_jwt=validate_jwt, revoke_jwt=revoke_jwt
    )


def jwt_verify_refresh_token_uc_dependency(
    validate_jwt: ValidateJwt = Depends(jwt_validation_dependency),
) -> VerifyRefreshTokenUseCase:
    return VerifyRefreshTokenUseCase(validate_jwt=validate_jwt)
