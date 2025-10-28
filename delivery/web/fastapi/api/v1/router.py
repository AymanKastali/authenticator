from fastapi import APIRouter

from delivery.web.fastapi.api.metadata.route_tags import RouteTag
from delivery.web.fastapi.api.v1.routes.auth.jwt import routes as jwt_routes
from delivery.web.fastapi.api.v1.routes.auth.registration import (
    routes as registration_routes,
)
from delivery.web.fastapi.api.v1.routes.auth.session import (
    routes as session_routes,
)
from delivery.web.fastapi.api.v1.routes.user_routes import routes as user_routes

v1_router = APIRouter(prefix="/api/v1")

auth_router = APIRouter(prefix="/auth", tags=[RouteTag.AUTH])
users_router = APIRouter(prefix="/users", tags=[RouteTag.USERS])

auth_routes = jwt_routes + session_routes + registration_routes

for route in auth_routes:
    route_dict = dict(vars(route).items())
    auth_router.add_api_route(**route_dict)

for route in user_routes:
    route_dict = dict(vars(route).items())
    users_router.add_api_route(**route_dict)

v1_router.include_router(auth_router)
v1_router.include_router(users_router)
