from adapters.presenters.response_models.success_item_response_model import (
    ItemResponseModel,
)
from delivery.web.fastapi.api.metadata.http_methods import HttpMethod
from delivery.web.fastapi.api.metadata.route_definitions import Route
from delivery.web.fastapi.api.metadata.route_tags import RouteTag
from delivery.web.fastapi.api.v1.endpoints.auth_endpoints import (
    jwt_login_endpoint,
    register_user_endpoint,
    session_login_endpoint,
)

routes = [
    Route(
        name="register_user",
        path="/register",
        status_code=201,
        methods=[HttpMethod.POST],
        endpoint=register_user_endpoint,
        tags=[RouteTag.AUTH],
        summary="Login User via Session",
        deprecated=False,
        response_model=ItemResponseModel[dict],
        description="Endpoint to login a user and receive a Session token.",
    ),
    Route(
        name="jwt_login_user",
        path="/login",
        status_code=200,
        methods=[HttpMethod.POST],
        endpoint=jwt_login_endpoint,
        tags=[RouteTag.AUTH],
        summary="Login User via JWT",
        deprecated=False,
        response_model=ItemResponseModel[dict],
        description="Endpoint to login a user and receive a JWT token.",
    ),
    Route(
        name="session_login_user",
        path="/login/session",
        status_code=200,
        methods=[HttpMethod.POST],
        endpoint=session_login_endpoint,
        tags=[RouteTag.AUTH],
        summary="Login User via Session",
        deprecated=False,
        response_model=ItemResponseModel[dict],
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
# POST   /auth/verify-email_address             # Verify email_address confirmation token
