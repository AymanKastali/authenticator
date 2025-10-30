from adapters.dto.responses.auth.jwt.me import ReadMeOutDto
from adapters.dto.responses.auth.jwt.payload import JwtTokenPayloadOutDto
from adapters.dto.responses.auth.jwt.tokens import JwtTokensOutDto
from adapters.dto.responses.generic.success.item import ItemOutDto
from delivery.web.fastapi.api.metadata.http_methods import HttpMethod
from delivery.web.fastapi.api.metadata.route_tags import RouteTag
from delivery.web.fastapi.api.v1.endpoints.auth.jwt.login import (
    jwt_login_endpoint,
)
from delivery.web.fastapi.api.v1.endpoints.auth.jwt.logout import (
    jwt_logout_endpoint,
)
from delivery.web.fastapi.api.v1.endpoints.auth.jwt.me import (
    read_me_endpoint,
)
from delivery.web.fastapi.api.v1.endpoints.auth.jwt.refresh_token import (
    refresh_jwt_token_endpoint,
)
from delivery.web.fastapi.api.v1.endpoints.auth.jwt.verify_token import (
    verify_jwt_token_endpoint,
)
from delivery.web.fastapi.api.v1.utils.routes_utils import create_route

_BASE = "/jwt"
_LOGIN = f"{_BASE}/login"
_REFRESH_TOKEN = f"{_BASE}/token/refresh"
_VERIFY_TOKEN = f"{_BASE}/token/verify"
_READ_ME = f"{_BASE}/me"
_LOGOUT = f"{_BASE}/logout"

routes = [
    create_route(
        name="jwt_login_user",
        path=_LOGIN,
        status_code=200,
        methods=[HttpMethod.POST],
        endpoint=jwt_login_endpoint,
        tag=RouteTag.AUTH,
        summary="Login UserEntity via JWT",
        response_model=ItemOutDto[JwtTokensOutDto],
        description="Endpoint to login a user and receive a JWT tokens.",
    ),
    create_route(
        name="jwt_refresh_token",
        path=_REFRESH_TOKEN,
        status_code=200,
        methods=[HttpMethod.POST],
        endpoint=refresh_jwt_token_endpoint,
        tag=RouteTag.AUTH,
        summary="Refresh JWT Token",
        response_model=ItemOutDto[JwtTokensOutDto],
        description="Endpoint to refresh a JWT Token and receive a JWT tokens.",
    ),
    create_route(
        name="jwt_verify_token",
        path=_VERIFY_TOKEN,
        status_code=200,
        methods=[HttpMethod.POST],
        endpoint=verify_jwt_token_endpoint,
        tag=RouteTag.AUTH,
        summary="Verify JWT Token",
        response_model=ItemOutDto[JwtTokenPayloadOutDto],
        description="Endpoint to Verify a JWT Token and receive a JWT Token Payload.",
    ),
    create_route(
        name="get_request_user",
        path=_READ_ME,
        status_code=200,
        methods=[HttpMethod.GET],
        endpoint=read_me_endpoint,
        tag=RouteTag.USERS,
        summary="Get my UserEntity info",
        response_model=ItemOutDto[ReadMeOutDto],
        description="Endpoint to get my own UserEntity info.",
    ),
    create_route(
        name="jwt_logout_user",
        path=_LOGOUT,
        status_code=204,
        methods=[HttpMethod.POST],
        endpoint=jwt_logout_endpoint,
        tag=RouteTag.AUTH,
        summary="Logout User via JWT",
        response_model=None,
        description="Endpoint to Logout a user.",
    ),
]

# POST   /auth/register                 # Register new user
# POST   /auth/login                    # Local login → JWT
# POST   /auth/token/refresh            # Refresh JWT
# POST   /auth/token/verify             # Verify JWT validity
# GET    /auth/me                       # Current authenticated user
# POST   /auth/login/session            # Local login → SessionEntity cookie

# POST   /auth/logout                   # Logout (JWT or session)

# GET    /auth/oauth/{provider}/login   # OAuth redirect (Google, GitHub, etc.)
# GET    /auth/oauth/{provider}/callback# OAuth callback
# POST   /auth/oauth/{provider}/link    # Link OAuth account to existing user

# POST   /auth/password/forgot          # Request password reset
# POST   /auth/password/reset           # Reset password with token
# POST   /auth/verify-email             # Verify email confirmation token
