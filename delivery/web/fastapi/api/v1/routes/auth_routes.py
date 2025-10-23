from adapters.presenters.response_models.jwt_response_model import (
    JwtResponseResponseModel,
)
from adapters.presenters.response_models.session_response_model import (
    SessionResponseModel,
)
from adapters.presenters.response_models.success_item_response_model import (
    ItemResponseModel,
)
from adapters.presenters.response_models.user_response_models import (
    RegisteredUserResponseModel,
)
from delivery.web.fastapi.api.metadata.http_methods import HttpMethod
from delivery.web.fastapi.api.metadata.route_tags import RouteTag
from delivery.web.fastapi.api.v1.endpoints.auth_endpoints import (
    jwt_login_endpoint,
    register_user_endpoint,
    session_login_endpoint,
)
from delivery.web.fastapi.api.v1.utils.routes_utils import create_route

_REGISTER = "/register"
_LOGIN_JWT = "/login/jwt"
_LOGIN_SESSION = "/login/session"

routes = [
    create_route(
        name="register_user",
        path=_REGISTER,
        status_code=201,
        methods=[HttpMethod.POST],
        endpoint=register_user_endpoint,
        tag=RouteTag.AUTH,
        summary="Login User via Session",
        response_model=ItemResponseModel[RegisteredUserResponseModel],
        description="Endpoint to login a user and receive a Session token.",
    ),
    create_route(
        name="jwt_login_user",
        path=_LOGIN_JWT,
        status_code=200,
        methods=[HttpMethod.POST],
        endpoint=jwt_login_endpoint,
        tag=RouteTag.AUTH,
        summary="Login User via JWT",
        response_model=ItemResponseModel[JwtResponseResponseModel],
        description="Endpoint to login a user and receive a JWT token.",
    ),
    create_route(
        name="session_login_user",
        path=_LOGIN_SESSION,
        status_code=200,
        methods=[HttpMethod.POST],
        endpoint=session_login_endpoint,
        tag=RouteTag.AUTH,
        summary="Login User via Session",
        response_model=ItemResponseModel[SessionResponseModel],
        description="Endpoint to login a user and receive a Session token.",
    ),
]

# POST   /auth/register                 # Register new user
# POST   /auth/login                    # Local login → JWT
# POST   /auth/login/session            # Local login → Session cookie

# POST   /auth/logout                   # Logout (JWT or session)
# POST   /auth/token/refresh            # Refresh JWT
# POST   /auth/token/verify             # Verify JWT validity
# GET    /auth/me                       # Current authenticated user

# GET    /auth/oauth/{provider}/login   # OAuth redirect (Google, GitHub, etc.)
# GET    /auth/oauth/{provider}/callback# OAuth callback
# POST   /auth/oauth/{provider}/link    # Link OAuth account to existing user

# POST   /auth/password/forgot          # Request password reset
# POST   /auth/password/reset           # Reset password with token
# POST   /auth/verify-email             # Verify email confirmation token
