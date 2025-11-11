from fastapi import Depends, HTTPException, status

from domain.exceptions.domain_errors import JwtRevokedError, UserNotFoundError
from infrastructure.exceptions.adapters_errors import (
    JwtExpiredError,
    JwtInvalidError,
)
from presentation.web.fastapi.api.v1.controllers.auth.jwt.get_authenticated_user import (
    GetAuthenticatedUserController,
)
from presentation.web.fastapi.api.v1.dependencies.controllers.jwt import (
    jwt_get_authenticated_user_controller_dependency,
)
from presentation.web.fastapi.api.v1.dependencies.security.oauth2 import (
    oauth2_scheme,
)
from presentation.web.fastapi.schemas.response.auth.jwt.authenticated_user import (
    AuthenticatedUserResponseSchema,
)


# -------------------- Current User Dependency --------------------
async def get_current_authenticated_user(
    token: str = Depends(oauth2_scheme),
    controller: GetAuthenticatedUserController = Depends(
        jwt_get_authenticated_user_controller_dependency
    ),
) -> AuthenticatedUserResponseSchema:
    """
    Returns the currently authenticated user.
    Raises 401 if token is invalid.
    """
    try:
        return await controller.execute(token)
    except (
        UserNotFoundError,
        JwtExpiredError,
        JwtInvalidError,
        JwtRevokedError,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        ) from e


# -------------------- Current Active User Dependency --------------------
def get_current_authenticated_active_user(
    current_user: AuthenticatedUserResponseSchema = Depends(
        get_current_authenticated_user
    ),
) -> AuthenticatedUserResponseSchema:
    """
    Returns the currently authenticated user only if active.
    Raises 403 if user is inactive.
    """
    if current_user.status.lower() != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return current_user
