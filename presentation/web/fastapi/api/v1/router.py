from fastapi import APIRouter

from presentation.web.fastapi.api.metadata.route_tags import RouteTag
from presentation.web.fastapi.api.v1.routes.auth.jwt import routes as jwt_routes
from presentation.web.fastapi.api.v1.routes.auth.registration import (
    routes as registration_routes,
)
from presentation.web.fastapi.api.v1.routes.auth.session import (
    routes as session_routes,
)
from presentation.web.fastapi.api.v1.routes.policies import (
    routes as policy_routes,
)
from presentation.web.fastapi.api.v1.routes.user_routes import (
    routes as user_routes,
)

v1_router = APIRouter(prefix="/api/v1")

auth_router = APIRouter(prefix="/auth", tags=[RouteTag.AUTH])
users_router = APIRouter(prefix="/users", tags=[RouteTag.USERS])
app_router = APIRouter(prefix="/app", tags=[RouteTag.APP])

auth_routes = jwt_routes + session_routes + registration_routes

for route in auth_routes:
    route_dict = dict(vars(route).items())
    auth_router.add_api_route(**route_dict)

for route in user_routes:
    route_dict = dict(vars(route).items())
    users_router.add_api_route(**route_dict)

for route in policy_routes:
    route_dict = dict(vars(route).items())
    app_router.add_api_route(**route_dict)

v1_router.include_router(app_router)
v1_router.include_router(auth_router)
v1_router.include_router(users_router)
