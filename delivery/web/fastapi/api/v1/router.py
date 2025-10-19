from fastapi import APIRouter

from delivery.web.fastapi.api.v1.routes.auth_routes import routes

v1_router = APIRouter(prefix="/api/v1")

for route in routes:
    route_dict = dict(vars(route).items())

    v1_router.add_api_route(**route_dict)
